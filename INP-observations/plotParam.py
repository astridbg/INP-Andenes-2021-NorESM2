import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':15})
import pandas as pd
from sklearn.linear_model import LinearRegression
from Meyers import meyers
import functions

homepath="/home/astridbg/Documents/nird/"

path = homepath+"observational_data/Coriolis_postprocessed/"
fname1 = "Coriolis_nucleiT_cal.csv"
fname2 = "Coriolis_nucleiOut_std.csv"
wpath = homepath+"INP-Andenes-2021-NorESM2/figures/"

# Must download dataset through correspondance with authors of 
# "The COMBLE Campaign: A Study of Marine Boundary Layer Clouds in Arctic Cold-Air Outbreaks",
# https://doi.org/10.1175/BAMS-D-21-0044.1
comble_path = "observational_data/comble_data.csv"

nucleiT = pd.read_csv(path+fname1, index_col=0)
nucleiOut = pd.read_csv(path+fname2, index_col=0)
nCor = len(nucleiT.iloc[0,:])

outlier_sample = 0
for i in range(nCor):
    nucleiT_i = nucleiT.iloc[:,i]
    nucleiOut_i = nucleiOut.iloc[:,i]
    if nucleiT_i.iloc[-2]>-10:
        if nucleiOut_i[np.where(nucleiT_i > -10)[0][0]] > 1e-2:
            outlier_sample = i
            print("Outlier: sample "+str(outlier_sample))

X = nucleiT.iloc[1:-1,:nCor].to_numpy() # I disclude the first and last well, as the concentration values here are not representative of reality
Y = nucleiOut.iloc[1:-1,:nCor].to_numpy()

X_ex1 = nucleiT.iloc[1:-1,:outlier_sample].to_numpy()
X_ex2 = nucleiT.iloc[1:-1,outlier_sample+1:nCor].to_numpy()
Y_ex1 = nucleiOut.iloc[1:-1,:outlier_sample].to_numpy()
Y_ex2 = nucleiOut.iloc[1:-1,outlier_sample+1:nCor].to_numpy()

X_ex = np.concatenate((X_ex1, X_ex2), axis=1)
Y_ex = np.concatenate((Y_ex1, Y_ex2), axis=1)

X = X.flatten()
Y = Y.flatten()
X_ex = X_ex.flatten()
Y_ex = Y_ex.flatten()

linreg = np.polyfit(X,np.log(Y), 1)
slope = linreg[0]
intercept = linreg[1]

linreg_ex = np.polyfit(X_ex,np.log(Y_ex), 1)
slope_ex = linreg_ex[0]
intercept_ex = linreg_ex[1]

print("With outlier:")
print(slope)
print(intercept)
print(functions.rsquared(X,np.log(Y)))
print("Without outlier:")
print(slope_ex)
print(intercept_ex)
print(functions.rsquared(X_ex,np.log(Y_ex)))

#-------------------------------
# Other parameterizations
#-------------------------------
# Li and Wieder
slope_L_W = -0.3504
intercept_L_W = -10.1826

# Sze

plt.figure(figsize=(8,6),dpi=300)
#plt.title("INP concentrations at Andenes 15.03$-$30.03 2021",fontsize=22)
plt.grid(alpha=0.5)
alpha=1

# Plot uncertainty estimate
err = 0.9

Tmin = []
Tmax = []
for j in range(95):
    Tmin.append(nucleiT.iloc[j,:].min()-err)
    Tmax.append(nucleiT.iloc[j,:].nlargest(2).min()+err)
conc = []
conc.append(nucleiOut.iloc[0,:].max())
for j in range(1,94):
    conc.append(nucleiOut.iloc[j,:].mean())
conc.append(nucleiOut.iloc[94,:].min())
plt.fill_betweenx(conc, Tmin, Tmax, color="lightblue", alpha=0.7)

# Plot excluding outlier sample
for i in range(0, outlier_sample):
    plt.scatter(nucleiT.iloc[:,i],nucleiOut.iloc[:,i], alpha = alpha, color="none", edgecolor="cornflowerblue")
    alpha -= 0.01
for i in range(outlier_sample+1, nCor):
    plt.scatter(nucleiT.iloc[:,i],nucleiOut.iloc[:,i], alpha = alpha, color="none", edgecolor="cornflowerblue")
    alpha -= 0.01

# Read COMBLE data
comble_data = pd.read_csv(comble_path)
plt.scatter(comble_data.iloc[:,0], comble_data.iloc[:,1],color='grey',s=10,alpha=0.8,marker="x")

plt.yscale("log")
plt.ylim(10**(-4.3),10**(1.8))
plt.xlim(-30,-2)
x = np.linspace(-30,-2,100)
# Plot parameterization without outlier 
plt.plot(x, np.exp(intercept_ex + slope_ex*x), linewidth=4, color="orange",
        label="\n Andenes 2021, \n exp("+str(round(intercept_ex,3))+" - "+str(round(np.sign(slope_ex)*slope_ex,3))+r"$\times T$)")
# Plot Meyers
plt.plot(x, meyers(x), linewidth=3, label="Meyers et al. (1992)",linestyle="dotted", color="red")
# Plot COMBLE data
plt.scatter(comble_data.iloc[0,0], comble_data.iloc[0,1], s=10,alpha=0.8,marker="x", label='Geerts et al. (2022), Andøy', color="grey")
# Plot Li and Wieder, with extra one to move legend name
plt.plot(x, np.exp(intercept_L_W + slope_L_W*x),linewidth=3,linestyle="dashdot",color="#ffffff",
        label=" ")
plt.plot(x, np.exp(intercept_L_W + slope_L_W*x),linewidth=3,linestyle="dashdot", color="darkblue",
        label="Li et al. (2023), Ny-Ålesund")
# Plot Sze study, winter and summer
plt.plot(x, 2.111*10**(-4)*np.exp(-0.263*x),linewidth=3,linestyle="dashed", color="springgreen",
        label="Sze et al. (2023), Greenland summer")
plt.plot(x, 4.711*10**(-7)*np.exp(-0.492*x),linewidth=3,linestyle="dashed", color="darkviolet",
        label="Sze et al. (2023), Greenland winter")
plt.plot(x, np.exp(intercept_ex + slope_ex*x), linewidth=4, color="orange")
plt.xlabel(r"Temperature $T$, $^{\circ}$C")
plt.ylabel(r"INP concentration, L$^{-1}$")

# Shrink current axis's height by 10% on the bottom
ax = plt.gca()
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)#,borderpad=0.3, columnspacing=0.3, handletextpad=0.2)

plt.savefig(wpath+"pdf/INPconc_param.pdf",bbox_inches="tight")
plt.savefig(wpath+"png/INPconc_param.png",bbox_inches="tight")

