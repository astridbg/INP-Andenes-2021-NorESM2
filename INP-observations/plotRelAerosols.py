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

homepath="/home/astridbg/Documents/nird/"

path_islas = homepath+"observational_data/"
path_cor = homepath+"observational_data/Coriolis_postprocessed/"
path_station = homepath+"observational_data/SN87110/"
path_temp = homepath+"observational_data/Inlet_Temp/"
path_aero = homepath+"observational_data/OPC_data/"
wpath = homepath+"observational_data/INP-Andenes-2021-NorESM2/figures/"

# -----------------------------
# Coriolis data
# -----------------------------

# Read in Coriolis INP concentrations

nucleiT = pd.read_csv(path_cor+"Coriolis_nucleiT_cal.csv",index_col=0)
nucleiT = nucleiT.drop(columns=['10'])
nCor = len(nucleiT.iloc[0,:])

# Read in Coriolis log file

df_cor = pd.read_csv(path_islas+"coriolis_log_all.csv", skiprows = 1)
df_cor = df_cor.drop(index=9)

t_start = pd.DataFrame(df_cor['Date'] + ' ' + df_cor['Start (UTC)'], columns = ['t_start'])
t_start = t_start.set_index('t_start')
t_start.index = pd.to_datetime(t_start.index, format = '%d-%m-%Y %H:%M')

t_end = pd.DataFrame(df_cor['Date'] + ' ' + df_cor['End (UTC)'], columns = ['t_end'])
t_end = t_end.set_index('t_end')
t_end.index = pd.to_datetime(t_end.index, format = '%d-%m-%Y %H:%M')


# Set time index to middle to sampling period

t_diff = datetime.timedelta(minutes=20)
t_middle = t_start.index + t_diff

df_frzT = nucleiT.iloc[1:-1].transpose()
df_frzT["mean_time"] = t_middle
df_frzT = df_frzT.set_index("mean_time")

# Get temperature at which fifty percent for all wells had frozen

index_50 = int(94/2)
t50 = df_frzT.iloc[:,index_50]


# -----------------------------
# Aerosol data
# -----------------------------

# Get pressure data

ds_pres = xr.open_dataset(path_station+"air_pressure_at_sea_level_202103.nc")
df_pres = ds_pres.to_dataframe()

# Get inlet temperature data

files = sorted(glob.glob(path_temp+"*.txt"))

count = 0
for f in files:

    df1 = pd.read_csv(f, delimiter = ',', parse_dates = ['Time'], index_col = ['Time'])
    if count == 0:
        df_temp = df1
    else:
        df_temp = pd.concat([df_temp, df1], axis = 0)

    count += 1

df_temp.to_csv("/projects/NS9600K/astridbg/data_INP-atm-present/Inlet_temperature.csv")

# Get OPC data

file_list = sorted(glob.glob(path_aero+"*/*.CSV"))
count = 0
for f in file_list:
    df1 = pd.read_csv(f, delimiter = ';', decimal = ',', parse_dates = ['Time'], index_col = ['Time'], keep_date_col = True)
    if count == 0:
        df_opc = df1
    else:
        df_opc = pd.concat([df_opc, df1])
        
    count += 1

df_opc.to_csv("/projects/NS9600K/astridbg/data_INP-atm-present/OPC_data.csv")
quit()

# Convert OPC data to standard litre

p_std = 1013.25
T_std = 273.15

df_opc["Count2 (/std_L)"] = df_opc["Count2 (/L)"]


for i in range(len(df_opc["Count2 (/L)"])):
   p = df_pres["air_pressure_at_sea_level"].iloc[df_pres.index.get_indexer([df_opc.index[i]], method="nearest")[0]]
   T = df_temp["Temperature(C)"].iloc[df_temp.index.get_indexer([df_opc.index[i]], method="nearest")[0]]
   df_opc["Count2 (/std_L)"][i] = df_opc["Count2 (/L)"][i] * p_std/p * (273.15 + T)/T_std

# Calculate aerosol surface area

def calc_surface_area(d):
    r = d/2
    sfc_area = 4*np.pi*r**2
    return sfc_area

df_opc["Total Surface Area"] = np.zeros(len(df_opc.iloc[:,0]))

for time in range(len(df_opc.iloc[:,0])):
    surface_area = 0
    for bin_size in [1,3,5,7,9]:
        size = df_opc.iloc[time,bin_size-1]
        #print("Size: ",size)
        aero_n = df_opc.iloc[time,bin_size]-df_opc.iloc[time,bin_size+2]
        #print("Total aerosol: ",df_opc.iloc[time,bin_size])
        #print("Aerosol bin size number: ",aero_n)
        surface_area += aero_n*calc_surface_area(size)
    bin_size = 11
    size = df_opc.iloc[time,bin_size-1]
    aero_n = df_opc.iloc[time,bin_size]
    #print("Size: ",size)
    #print("Total aerosol: ",df_opc.iloc[time,bin_size])
    #print("Aerosol bin size number: ",aero_n)
    surface_area += aero_n*calc_surface_area(size)
    df_opc["Total Surface Area"][time] = surface_area

# -----------------------------
# Averages over Coriolis period
# -----------------------------

sfc_all = []
opc_all = []

# For full-length datasets
i = 1
for cor in t_start.index:

    print(cor.date(),", Coriolis sample: ",i)

    time_opc = df_opc.loc[str(cor.date())].index.hour
    index_cor_opc = np.where(np.logical_or(time_opc == cor.hour, time_opc == int(cor.hour + cor.minute/60. + 40./60.)))
    sfc = np.nanmean(np.array(df_opc['Total Surface Area'][str(cor.date())])[index_cor_opc])
    opc = np.nanmean(np.array(df_opc['Count2 (/std_L)'][str(cor.date())])[index_cor_opc])

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

df_opc["Count2 (/std_L)"].plot(ax=axs[1,0],label="Particles $\geq 0.5 \mu$m",zorder=1)
axs[1,0].scatter(df_frzT.index,opc_all,color="orange",zorder=2)
axs[1,0].set_xbound(xlims[0],xlims[1])
axs[1,0].set_xticks(xticks)
axs[1,0].set_xticklabels([])
axs[1,0].grid()
axs[1,0].set_yscale("log")
#axs[1,0].set_ylim([5,1e+6])
axs[1,0].xaxis.set_minor_locator(mpl.ticker.NullLocator())
axs[1,0].set_ylabel("#/L$_{std}$")
axs[1,0].set_xlabel(None)
axs[1,0].set_title("Concentration of particles $\geq 0.5 \mu$m")
#axs[1,0].legend(loc="upper left",frameon=False)
axs[1,0].annotate("(b)",fontsize=25,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(-30, 20), textcoords='offset points',
                ha='left', va='top')


axs[1,1].scatter(t50,opc_all,color="orange")
axs[1,1].grid(alpha=0.5)
axs[1,1].set_ylabel("Particles $\geq 0.5 \mu$m (#/L$_{std}$)")
#axs[1,1].set_xlabel("Temperature at 50 % \n frozen fraction ($^{\circ}$C)")
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

df_opc["Total Surface Area"].plot(ax=axs[2,0],label="Particles $\geq 0.5 \mu$m",zorder=1)
axs[2,0].scatter(df_frzT.index,sfc_all,color="orange",zorder=2)
axs[2,0].set_xbound(xlims[0],xlims[1])
axs[2,0].set_xticks(xticks)
#axs[2,0].set_xticklabels([])
axs[2,0].grid()
axs[2,0].set_yscale("log")
#axs[1,0].set_ylim([5,1e+6])
axs[2,0].xaxis.set_minor_locator(mpl.ticker.NullLocator())
axs[2,0].set_ylabel("m$^2$/L$_{std}$")
axs[2,0].set_xlabel(None)
axs[2,0].set_title("Total Surface Area of Aerosols")
#axs[1,0].legend(loc="upper left",frameon=False)
axs[2,0].annotate("(c)",fontsize=25,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(-30, 20), textcoords='offset points',
                ha='left', va='top')

axs[2,1].scatter(t50,sfc_all,color="orange")
axs[2,1].grid(alpha=0.5)
axs[2,1].set_ylabel("m$^2$/L$_{std}$")
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
