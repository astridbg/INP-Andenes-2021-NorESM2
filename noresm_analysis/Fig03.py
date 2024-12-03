import xarray as xr
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
# Set font style to match latex document----------
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':20})
# ------------------------------------------------
import cartopy.crs as ccrs
import functions

rpath="../../model_data/noresm_postprocessed/"
wpath="../figures/"

# Default cases----------------
case1 = "M92_20241122"; case1nm = "M92"
# Modified cases---------------
case2 = "A21_20241125"; case2nm = "A21"
#------------------------------	
date1 = "2007-04-15_2010-03-15"
date2 = "2007-04-15_2010-03-15"

#------------------------------
# Add open ocean mask
#------------------------------
ocean_mask = False
if ocean_mask:
    ds_ocn = xr.open_dataset(rpath+"OCNFRAC"+"_"+case2+"_"+date2+".nc")
    open_sea = ds_ocn > 0.85
    open_sea = open_sea.mean("time")
    open_sea = open_sea >= 0.5

#------------------------------
# Two three-dimensional fields
# with specific level
#------------------------------

var_level = 850
concentrations = ["NUMICE"]
variables = [["FREQI", "NUMICE"]]
plot_titles = [["Ice cloud fractional occurence", 
                "Grid-box averaged \n cloud ice number conc. (1/kg)",
                "Relative change in \n cloud ice number conc. \n at 859 hPa"]]

#------------------------------
# Titles
#------------------------------

for var, titles in zip(variables, plot_titles):
      # Open datasets for both variables 
      var_xtra = var[0]
      var = var[1]
      ds1 = xr.open_dataset(rpath+var+"_"+case1+"_"+date1+".nc")
      ds2 = xr.open_dataset(rpath+var+"_"+case2+"_"+date2+".nc")
      ds1_xtra = xr.open_dataset(rpath+var_xtra+"_"+case1+"_"+date1+".nc")
      ds2_xtra = xr.open_dataset(rpath+var_xtra+"_"+case2+"_"+date2+".nc")

      var1_name = titles[0]
      var2_name = titles[1]
      map_title = titles [2]
      
      # Get start and end date of period
      date_start = str(ds1.time[0].values).split(" ")[0]
      date_end = str(ds1.time[-1].values).split(" ")[0]

      # Get the time average of cases over the whole period
      ds1m = ds1.mean("time")
      ds2m = ds2.mean("time")

      # Select level
      ds1_level = ds1m.sel(lev=var_level, method="nearest")
      ds2_level = ds2m.sel(lev=var_level, method="nearest")
      lev_name = str(int(ds1_level.lev.values))

      # Get relative difference between cases time averaged over the whole period
      diff = ds2_level[var]-ds1_level[var]
      reldiff = diff/ds1_level[var].where(ds1_level[var]!=0)*100*np.sign(ds1_level[var])

      lev_extent = round(max(abs(np.nanmin(reldiff.sel(lat=slice(66.5,90)).values)), 
                              abs(np.nanmax(reldiff.sel(lat=slice(66.5,90)).values))))
      lev_extent = 50
      levels = np.linspace(-lev_extent,lev_extent,25)

      # Make horizontal averages:
      # - for the Arctic
      ds1_arct_height = functions.computeWeightedMean(ds1m[var].sel(lat=slice(66.5,90),lev=slice(350, 1000)))
      ds2_arct_height = functions.computeWeightedMean(ds2m[var].sel(lat=slice(66.5,90),lev=slice(350, 1000)))
      
      ds1_xtra_arct = functions.computeWeightedMean(ds1_xtra[var_xtra].mean("time").sel(lat=slice(66.5,90),lev=slice(350, 1000)))
      ds2_xtra_arct = functions.computeWeightedMean(ds2_xtra[var_xtra].mean("time").sel(lat=slice(66.5,90),lev=slice(350, 1000)))

      height_levels = ds1.lev.sel(lev=slice(350, 1000)).values

      fig  = plt.figure(figsize=[18,7],dpi=300)
      
      ax0 = plt.subplot(1, 3, 1)
      plt.plot(ds1_xtra_arct, height_levels, label=case1nm, color="tab:blue",linestyle="--",linewidth=2)
      plt.plot(ds2_xtra_arct, height_levels, label=case2nm, color="tab:orange",linewidth=2)
      plt.hlines(ds1_level.lev.values, ax0.get_xlim()[0],ax0.get_xlim()[1], color="black",linestyle=":")
      if var_xtra in concentrations:
         plt.xscale("log")
      plt.ylabel("hPa")
      #plt.xlabel(ds1_xtra[var_xtra].long_name+", "+ds1_xtra[var_xtra].units)
      plt.xlabel(var1_name)
      plt.legend(loc="upper left",frameon=True,title="Arctic averages",fancybox=False)
      plt.grid(alpha=0.5)
      ax0.invert_yaxis()
      ax0.annotate("(a)",fontsize=25,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(-30, 20), textcoords='offset points',
                ha='left', va='top')

      ax1 = plt.subplot(1, 3, 2)
      plt.plot(ds1_arct_height, height_levels, label=case1nm, color="tab:blue",linestyle="--",linewidth=2)
      plt.plot(ds2_arct_height, height_levels, label=case2nm, color="tab:orange",linewidth=2)
      plt.hlines(ds1_level.lev.values, ax1.get_xlim()[0],ax1.get_xlim()[1], color="black",linestyle=":")
      #plt.hlines(ds1_level.lev.values, 1,ax1.get_xlim()[1], color="black",linestyle=":")
      if var in concentrations:
         plt.xscale("log")
      #plt.ylabel("hPa")
      plt.yticks(np.arange(400, 1100, 100), labels=[])
      #plt.xlabel(ds1[var].long_name+", "+ds1[var].units)
      plt.xlabel(var2_name)

      #plt.xticks([1, 10])
      #plt.legend(loc="upper left",frameon=True,title="Arctic averages",fancybox=False)
      plt.grid(alpha=0.5)
      ax1.invert_yaxis()
      ax1.annotate("(b)",fontsize=25,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(-30, 20), textcoords='offset points',
                ha='left', va='top')

      ax2 = plt.subplot(1,3,3, projection=ccrs.Orthographic(0, 90))
      functions.polarCentral_set_latlim([66.5,90], ax2)
      map = reldiff.plot.pcolormesh(ax=ax2, transform=ccrs.PlateCarree(), 
                                             cmap="coolwarm",#cmap=plt.cm.get_cmap('Blues').reversed(), #cmap="coolwarm"
                                             levels=levels,
                                             add_colorbar=False)

      ax2.coastlines()
      ax2.annotate("(c)",fontsize=25,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(-30, 68), textcoords='offset points',
                ha='left', va='top')
      if ocean_mask:
            ax2.contourf(open_sea.lon, open_sea.lat, open_sea["OCNFRAC"], transform=ccrs.PlateCarree(), colors='none',hatches=['..'],levels=[.5, 1.5])
      #ax2.set_title("Relative change in\n"+ds1[var].long_name, fontsize=20) 
      ax2.set_title(map_title, fontsize=20)
      cb_ax = fig.add_axes([0.66, 0.11, 0.27, 0.04])

      cbar = plt.colorbar(map, cax=cb_ax, spacing = 'uniform', extend='both', orientation='horizontal', fraction=0.046, pad=0.06)
      #cbar.ax.tick_params(labelsize=18)
      cbar.ax.set_xlabel("%")#, fontsize=23)
      if lev_extent >= 4:
         cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places        
      elif 0.4 <= lev_extent < 4:
         cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}')) # One decimal place
      elif 0.04 <= lev_extent < 0.4:
         cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}')) # Two decimal places     
      elif 0.004 <= lev_extent < 0.04:
         cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}')) # Three decimal places
      

      #plt.savefig(wpath+"pdf/"+var+"_"+var_xtra+"_heightplusrelhoriz_"+lev_name+"_"+case1+"_"+case2+".pdf",bbox_inches="tight")
      #plt.savefig(wpath+"png/"+var+"_"+var_xtra+"_heightplusrelhoriz_"+lev_name+"_"+case1+"_"+case2+".png",bbox_inches="tight")
      plt.savefig(wpath+"pdf/Fig03.pdf",bbox_inches="tight")
      plt.savefig(wpath+"png/Fig03.png",bbox_inches="tight")
      plt.clf()	

