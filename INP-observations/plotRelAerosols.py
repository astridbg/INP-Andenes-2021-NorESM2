# Author: Tim Carlsen
# Modified by: Astrid Bragstad Gjelsvik

import numpy as np
import pandas as pd
import xarray as xr
import glob
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
import functions
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':20})

path_cor = "../../observational_data/"
wpath = "../figures/"

# -----------------------------
# Coriolis data
# -----------------------------

# Read in Coriolis INP freezing temperatures

nucleiT = pd.read_csv(path_cor+"Coriolis_nucleiT_cal.csv",index_col=0)
nucleiT = nucleiT.drop(columns=['10']) # Remove outlier measurement

# Read in Coriolis log file

df_cor = pd.read_csv(path_islas+"coriolis_log_all.csv", skiprows = 1)
df_cor = df_cor.drop(index=9)

t_start = pd.DataFrame(df_cor['Date'] + ' ' + df_cor['Start (UTC)'], columns = ['t_start'])
t_start = t_start.set_index('t_start')
t_start.index = pd.to_datetime(t_start.index, format = '%d-%m-%Y %H:%M')

# Set time index to middle to sampling period

t_diff = datetime.timedelta(minutes=20) # Each INP measurement takes 40 min
t_middle = t_start.index + t_diff

df_frzT = nucleiT.transpose()

df_frzT["mean_time"] = t_middle
df_frzT = df_frzT.set_index("mean_time")

# Get temperature at which fifty percent for all wells had frozen

index_50 = int(96/2)
t50 = df_frzT.iloc[:,index_50]

# -----------------------------
# Aerosol data
# -----------------------------

# Read OPC data
ds_opc = xr.open_dataset(path_islas+"opc_islas2021_final.nc")

# Calculate aerosol surface area

def calc_surface_area(d):
    # Assume spherical particles
    r = d/2
    sfc_area = 4*np.pi*r**2
    return sfc_area

total_surface_area_geq_500nm = np.zeros(len(ds_opc.time))

for t in range(len(ds_opc.time)):
    # Calculate surface area for new time step
    surface_area = 0
    
    # Calculate surface area for individual bin sizes
    for i in range(1,len(ds_opc.particle_size_bin)-1): # Only include particles >= 500 nm
        size=float(ds_opc.particle_size_bin[i])
        #print("Size: ",size)
        total_aerosol_geq_this_size = float(ds_opc.particle_number_concentration.isel(time=t,particle_size_bin=i))
        total_aerosol_g_this_size = float(ds_opc.particle_number_concentration.isel(time=t,particle_size_bin=i+1))
        particle_n = total_aerosol_geq_this_size - total_aerosol_g_this_size
        #print("Total aerosol: ",total_aerosol_geq_this_size)
        #print("Aerosol bin size number: ",particle_n)
        surface_area += particle_n*calc_surface_area(size)
    
    # Calculate surface for last bin
    size=float(ds_opc.particle_size_bin[5])
    #print("Size: ",size)
    # Assume that all particles >= 3000 nm are all 3000 nm
    particle_n = float(ds_opc.particle_number_concentration.isel(time=t,particle_size_bin=5))
    #print("Aerosol bin size number: ",particle_n)
    surface_area += particle_n*calc_surface_area(size)
    total_surface_area_geq_500nm[t] = surface_area

# -----------------------------
# Averages over Coriolis period
# -----------------------------

sfc_all = []
opc_all = []

df_opc = ds_opc.particle_number_concentration.isel(particle_size_bin=1).to_dataframe()
df_opc['total_surface_geq_500nm'] = total_surface_area_geq_500nm

# For full-length datasets
i = 1
for cor in t_start.index:

    print(cor.date(),", Coriolis sample: ",i)

    time_opc = df_opc.loc[str(cor.date())].index.hour
    index_cor_opc = np.where(np.logical_or(time_opc == cor.hour, time_opc == int(cor.hour + cor.minute/60. + 40./60.)))
    opc = np.nanmean(np.array(df_opc['particle_number_concentration'][str(cor.date())])[index_cor_opc])
    sfc = np.nanmean(np.array(df_opc['total_surface_geq_500nm'][str(cor.date())])[index_cor_opc])

    opc_all = np.append(opc_all, opc)
    sfc_all = np.append(sfc_all, sfc)

    i += 1

# -----------------------------
# Plotting routine
# -----------------------------

fig, axs = plt.subplots(3, 2, gridspec_kw={'width_ratios': [4, 1]}, figsize=(12,9), dpi=300, constrained_layout=True)

df_frzT.T.boxplot(
        positions=mpl.dates.date2num(df_frzT.index),
        widths=0.1, flierprops = dict(marker='.',markeredgecolor="tab:blue"), ax=axs[0,0])
locator = mpl.dates.AutoDateLocator(minticks=10, maxticks=15)
axs[0,0].xaxis.set_major_locator(locator)
axs[0,0].set_xticklabels([])
xlims = mpl.dates.num2date(axs[0,0].get_xlim())
xticks = mpl.dates.num2date(axs[0,0].get_xticks())
axs[0,0].set_ylabel("$^{\circ}$C")
axs[0,0].set_title("Freezing temperatures of INPs")
axs[0,0].annotate("(a)",fontsize=25,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(-30, 20), textcoords='offset points',
                ha='left', va='top')

df_opc["particle_number_concentration"].plot(ax=axs[1,0],label="Particles $\geq 0.5 \mu$m",zorder=1)
axs[1,0].scatter(df_frzT.index,opc_all,color="orange",zorder=2)
axs[1,0].set_xbound(xlims[0],xlims[1])
axs[1,0].set_xticks(xticks)
axs[1,0].set_xticklabels([])
axs[1,0].grid()
axs[1,0].set_yscale("log")
axs[1,0].xaxis.set_minor_locator(mpl.ticker.NullLocator())
axs[1,0].set_ylabel("L$^{-1}$")
axs[1,0].set_xlabel(None)
axs[1,0].set_title("Concentration of particles $\geq 0.5 \mu$m")
axs[1,0].annotate("(b)",fontsize=25,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(-30, 20), textcoords='offset points',
                ha='left', va='top')


axs[1,1].scatter(t50,opc_all,color="orange")
axs[1,1].grid(alpha=0.5)
axs[1,1].set_ylabel("Particles $\geq 0.5\mu$m (L$^{-1}$)")
axs[1,1].set_yscale("log")
axs[1,1].annotate("R: %.2f, R$^2$: %.2f" %(functions.r(t50,opc_all),functions.rsquared(t50,opc_all)),
                xy=(0, 1), xycoords='axes fraction',
                xytext=(5, 16), textcoords='offset points',
                ha='left', va='top')
axs[1,1].annotate("(d)",fontsize=25,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(-30, 20), textcoords='offset points',
                ha='left', va='top')

fig.delaxes(axs[0,1])

df_opc["total_surface_geq_500nm"].plot(ax=axs[2,0],zorder=1)
axs[2,0].scatter(df_frzT.index,sfc_all,color="orange",zorder=2)
axs[2,0].set_xbound(xlims[0],xlims[1])
axs[2,0].set_xticks(xticks)
axs[2,0].grid()
axs[2,0].set_yscale("log")
axs[2,0].xaxis.set_minor_locator(mpl.ticker.NullLocator())
axs[2,0].set_ylabel("$\mu$m$^2$L$^{-1}$")
axs[2,0].set_xlabel(None)
axs[2,0].set_title("Total Surface Area of Aerosols")
axs[2,0].annotate("(c)",fontsize=25,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(-30, 20), textcoords='offset points',
                ha='left', va='top')

axs[2,1].scatter(t50,sfc_all,color="orange")
axs[2,1].grid(alpha=0.5)
axs[2,1].set_ylabel("$\mu$m$^2$L$^{-1}$")
axs[2,1].set_yscale("log")
axs[2,1].annotate("R: %.2f, R$^2$: %.2f" %(functions.r(t50,sfc_all),functions.rsquared(t50,sfc_all)),
                xy=(0, 1), xycoords='axes fraction',
                xytext=(5, 16), textcoords='offset points',
                ha='left', va='top')
axs[2,1].annotate("(e)",fontsize=25,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(-30, 20), textcoords='offset points',
                ha='left', va='top')
axs[2,1].set_xlabel("Temperature at 50 % \n frozen fraction ($^{\circ}$C)")

plt.savefig(wpath+"pdf/aerosol_corr.pdf", bbox_inches="tight")
plt.savefig(wpath+"png/aerosol_corr.png", bbox_inches="tight")
