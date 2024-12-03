import matplotlib.pyplot as plt
import matplotlib
import xarray as xr
import numpy as np
import pandas as pd
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':15})
from Meyers import meyers
import functions

rpath = "../../aerosol_data/"
rpath2 = "../../other_observations/"
figpath = "../figures/"

# Read INP data
ds = xr.open_dataset(rpath+'INP_data_ISLAS21.nc')

# Read COMBLE data from Geerts et al. (2022), https://doi.org/10.1175/BAMS-D-21-0044.1
# Can be provided upon request
comble_path = rpath2+"COMBLE_INP_DATA.csv"
comble_data = pd.read_csv(comble_path)

#-------------------------------
# Create parameterization
#-------------------------------

X = np.array(ds.freezing_temperatures)
Y = np.array(ds.INP_concentrations)

linreg = np.polyfit(X,np.log(Y), 1)
slope = linreg[0]
intercept = linreg[1]

print("PARAMETERIZATION")
print("Slope: ",slope)
print("Intercept: ", intercept)
print("R-squared: ", functions.rsquared(X,np.log(Y)))

#-------------------------------
# Other parameterizations
#-------------------------------
# Li and Wieder, https://doi.org/10.5194/acp-22-14441-2022
slope_L_W = -0.3504
intercept_L_W = -10.1826

# Sze et al. (2023), https://doi.org/10.5194/acp-23-4741-2023
# Summer
slope_S_s = -0.263
intercept_S_s= 2.111*10**(-4)
# Winter
slope_S_w = -0.492
intercept_S_w = 4.711*10**(-7)

#-------------------------------
# Plotting
#-------------------------------

x = np.linspace(-30,-2,100)
plt.figure(figsize=(8,6),dpi=300)
plt.grid(alpha=0.5)

# Plot uncertainty estimate
err = 0.9
for i in range(len(Y)):
    plt.hlines(Y[i],X[i]-err,X[i]+err,color="lightblue", alpha=0.7,zorder=1)

# Plot INP measurements excluding outlier
plt.scatter(X, Y,color="none", edgecolor="cornflowerblue",zorder=2)

# Read COMBLE data
plt.scatter(comble_data.iloc[:,0], comble_data.iloc[:,1],color='grey',s=10,alpha=0.8,marker="x",zorder=3)

# Plot parameterization without outlier 
plt.plot(x, np.exp(intercept + slope*x), linewidth=4, color="orange", zorder=6,
        label="\n Andenes 2021, \n exp("+str(round(intercept,3))+" - "+str(round(np.sign(slope)*slope,3))+r"$\times T$)")

# Plot Meyers
plt.plot(x, meyers(x), linewidth=3, label="Meyers et al. (1992)",linestyle="dotted", color="red")

# Plot COMBLE data, one extra time for legend
plt.scatter(comble_data.iloc[:,0], comble_data.iloc[:,1],color='grey',s=10,alpha=0.8,marker="x",zorder=3)
plt.scatter(comble_data.iloc[0,0], comble_data.iloc[0,1], s=10,alpha=0.8,marker="x", 
            label='Geerts et al. (2022), Andøy', color="grey")

# Plot Li and Wieder
plt.plot(x, np.exp(intercept_L_W + slope_L_W*x),linewidth=6, linestyle="dashdot", color="darkblue",
        label="Li et al. (2023), Ny-Ålesund",zorder=5)

# Plot Sze study, winter and summer

plt.plot(x, intercept_S_s*np.exp(slope_S_s*x),linewidth=3,linestyle="dashed", color="springgreen",
        label="Sze et al. (2023), Greenland summer",zorder=4)
plt.plot(x, intercept_S_w*np.exp(slope_S_w*x),linewidth=3,linestyle="dashed", color="darkviolet",
        label="Sze et al. (2023), Greenland winter",zorder=5)

plt.xlabel(r"Temperature $T$, $^{\circ}$C")
plt.ylabel(r"INP concentration, L$^{-1}$")
plt.yscale("log")
plt.ylim(10**(-4.3),10**(1.8))
plt.xlim(-30,-2)

# Shrink current axis's height by 10% on the bottom
ax = plt.gca()
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)#,borderpad=0.3, columnspacing=0.3, handletextpad=0.2)

plt.savefig(figpath+"pdf/Fig02.pdf",bbox_inches="tight")
plt.savefig(figpath+"png/Fig02.png",bbox_inches="tight")


