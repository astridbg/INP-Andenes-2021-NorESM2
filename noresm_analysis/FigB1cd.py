import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from cmcrameri import cm
# Set font style to match latex document----------
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':20})
# ------------------------------------------------
import datetime
from functions import *

rpath="../../model_data/noresm_postprocessed/"
wpath="../figures/"

# Default case----------------
case1 = "M92_20241122"; case1nm = "M92"
# Modified case---------------
case2 = "A21_20241125"; case2nm = "A21"
#------------------------------	
date1 = "2007-04-15_2010-03-15"
date2 = "2007-04-15_2010-03-15"

#------------------------------
# Areas to analyse
#------------------------------

NYA = [78.9227, 11.9273] # Ny-Ålesund
ALE = [82.5, 297.6] # Alert
BAR = [71.17, 203.55] # Barrow
npole = [[0,360],[85,90]] # North Pole

#------------------------------
# Two-dimensional fields
#------------------------------

variables = ["CLDTOT"]

#------------------------------
# Plotting monthly mean averages
#------------------------------
for var in variables:
    print(var)
    ds1 = xr.open_dataset(rpath+var+"_"+case1+"_"+date1+".nc")
    ds2 = xr.open_dataset(rpath+var+"_"+case2+"_"+date2+".nc")
	
    # Get start and end date of period
    date_start = str(ds1.time[0].values).split(" ")[0]
    date_end = str(ds1.time[-1].values).split(" ")[0]

    # Get monthly mean
    ds1m = ds1.groupby("time.month").mean("time")
    ds2m = ds2.groupby("time.month").mean("time")
	
    # Make time array
    months = []
    for i in range(len(ds1m.month.values)):
        datetime_object = datetime.datetime.strptime(str(ds1m.month.values[i]), "%m")
        months.append(datetime_object.strftime("%b"))
	
    # Get spatial average over Arctic
    ds1_arct = computeWeightedMean(ds1m[var].sel(lat=slice(66.5,90)))
    ds2_arct = computeWeightedMean(ds2m[var].sel(lat=slice(66.5,90)))
    print("Arctic")
    print("Difference",(ds2_arct-ds1_arct).mean("month").values)
    print("Case 1",ds1_arct.mean("month").values)
    print("Case 2",ds2_arct.mean("month").values)

    # Get values over Ny-Ålesund
    ds1_NYA = ds1m[var].sel(lat=NYA[0], lon=NYA[1], method="nearest")
    ds2_NYA = ds2m[var].sel(lat=NYA[0], lon=NYA[1], method="nearest")

    # Get values over Alert
    ds1_ALE = ds1m[var].sel(lat=ALE[0], lon=ALE[1], method="nearest")
    ds2_ALE = ds2m[var].sel(lat=ALE[0], lon=ALE[1], method="nearest")

    # Get values over Barrow
    ds1_BAR = ds1m[var].sel(lat=BAR[0], lon=BAR[1], method="nearest")
    ds2_BAR = ds2m[var].sel(lat=BAR[0], lon=BAR[1], method="nearest")
        
    # Get spatial average over North Pole
    ds1_npol = computeWeightedMean(ds1m[var].sel(lon=slice(npole[0][0],npole[0][1]),
                                 lat=slice(npole[1][0],npole[1][1])))
    ds2_npol = computeWeightedMean(ds2m[var].sel(lon=slice(npole[0][0],npole[0][1]),
                                 lat=slice(npole[1][0],npole[1][1])))

    print("North Pole")
    print((ds2_npol-ds1_npol).mean("month").values)

    print("Ny_Ålesund")
    print((ds2_NYA-ds1_NYA).mean("month").values)

    print("Alert")
    print((ds2_ALE-ds1_ALE).mean("month").values)

    print("Barrow")
    print((ds2_BAR-ds1_BAR).mean("month").values)
     
    fig,axs = plt.subplots(ncols=2,nrows=1, gridspec_kw={'width_ratios': [3, 1]}, figsize=[13,4],dpi=300,constrained_layout=True)
    ax = axs[0]
    ax2 = axs[1]

    ax.plot(months, ds2_arct-ds1_arct, color=cm.romaO.colors[0], label="Arctic")
    ax.plot(months, ds2_NYA-ds1_NYA, color=cm.romaO.colors[49], label="Ny-Ålesund")
    ax.plot(months, ds2_ALE-ds1_ALE, color=cm.romaO.colors[99], label="Alert")
    ax.plot(months, ds2_BAR-ds1_BAR, color=cm.romaO.colors[149], label="Utqiagvik")
    ax.plot(months, ds2_npol-ds1_npol, color=cm.romaO.colors[199], label="North Pole")
    ax.set_ylabel(r"$\Delta$"+ds1[var].units)
    ax.tick_params(axis="x",labelsize=20)
    ax.grid(alpha=0.5)

    if var == "TREFHT":
        # Get average absolute change
         
        abs_arct = ds2_arct-ds1_arct
        abs_nya = ds2_NYA-ds1_NYA
        abs_ale = ds2_ALE-ds1_ALE
        abs_bar = ds2_BAR-ds1_BAR
        abs_npol = ds2_npol-ds1_npol
    
    
        change_all = pd.DataFrame({"Arctic":abs_arct,"Ny-Ålesund":abs_nya,"Alert":abs_ale,"Utqiagvik":abs_bar,"North Pole":abs_npol})
        bplot=ax2.boxplot(change_all,patch_artist=True,medianprops={"color":"black"})
        ax2.set_ylabel(r"$\Delta$"+ds1[var].units)
    
    elif var == "TGCLDLWP" or var == "TGCLDIWP":

        # Get average relative change
        # Shrink y axis due to extreme values

        rel_arct = ((ds2_arct-ds1_arct)/ds1_arct.where(ds1_arct!=0)).fillna(0)*100*np.sign(ds1_arct)
        rel_nya = ((ds2_NYA-ds1_NYA)/ds1_NYA.where(ds1_NYA!=0)).fillna(0)*100*np.sign(ds1_NYA)
        rel_ale = ((ds2_ALE-ds1_ALE)/ds1_ALE.where(ds1_ALE!=0)).fillna(0)*100*np.sign(ds1_ALE)
        rel_bar = ((ds2_BAR-ds1_BAR)/ds1_BAR.where(ds1_BAR!=0)).fillna(0)*100*np.sign(ds1_BAR)
        rel_npol = ((ds2_npol-ds1_npol)/ds1_npol.where(ds1_npol!=0)).fillna(0)*100*np.sign(ds1_npol)
    
    
        rel_all = pd.DataFrame({"Arctic":rel_arct,"Ny-Ålesund":rel_nya,"Alert":rel_ale,"Utqiagvik":rel_bar,"North Pole":rel_npol})
        bplot=ax2.boxplot(rel_all,patch_artist=True,medianprops={"color":"black"},showfliers=False)
        ax2.set_ylabel("% change")
        ax2.set_yscale("log")
        print(rel_arct)
        print("Arctic annual average relative change (%): ", np.mean(rel_arct))


    else:
        # Get average relative change
    
        rel_arct = ((ds2_arct-ds1_arct)/ds1_arct.where(ds1_arct!=0)).fillna(0)*100*np.sign(ds1_arct)
        rel_nya = ((ds2_NYA-ds1_NYA)/ds1_NYA.where(ds1_NYA!=0)).fillna(0)*100*np.sign(ds1_NYA)
        rel_ale = ((ds2_ALE-ds1_ALE)/ds1_ALE.where(ds1_ALE!=0)).fillna(0)*100*np.sign(ds1_ALE)
        rel_bar = ((ds2_BAR-ds1_BAR)/ds1_BAR.where(ds1_BAR!=0)).fillna(0)*100*np.sign(ds1_BAR)
        rel_npol = ((ds2_npol-ds1_npol)/ds1_npol.where(ds1_npol!=0)).fillna(0)*100*np.sign(ds1_npol)
    
    
        rel_all = pd.DataFrame({"Arctic":rel_arct,"Ny-Ålesund":rel_nya,"Alert":rel_ale,"Utqiagvik":rel_bar,"North Pole":rel_npol})
        bplot=ax2.boxplot(rel_all,patch_artist=True,medianprops={"color":"black"},showfliers=False)
        ax2.set_ylabel("% change")
    
    colors=cm.romaO.colors[::50][:5]
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    ax2.set_xticklabels([])

    # Shrink current axis's height by 15% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.15,
                     box.width, box.height * 0.85])
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0 + box.height * 0.15,
                     box.width, box.height * 0.85])

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.75, -0.12), ncol=5, columnspacing=0.5, handlelength=1,handletextpad=0.4)
	
    plt.grid(alpha=0.5)
    plt.savefig(wpath+"pdf/"+var+"_avg_"+case1+"_"+case2+".pdf",bbox_inches="tight")
    plt.savefig(wpath+"png/"+var+"_avg_"+case1+"_"+case2+".png",bbox_inches="tight")
    plt.clf()
