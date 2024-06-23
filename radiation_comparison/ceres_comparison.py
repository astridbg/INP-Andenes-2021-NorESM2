import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
# Set font style to match latex document----------
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':20})
# ------------------------------------------------
from functions import *

homepath="/home/astridbg/Documents/nird/" # Change to suitable path

# Paths to data
ceres_path = "/projects/NS9600K/astridbg/observational_data/radiation/CERES_EBAF_Ed4.2_Subset_200704-201003.nc" # Data must be downloaded from https://search.earthdata.nasa.gov/
noresm_path = homepath+"model_data/noresm_postprocessed/"

# Paths to figures
fig_path = homepath+"INP-Andenes-2021-NorESM2/figures/"

#-------------------------------------
# CERES Uncertainty
# https://ceres.larc.nasa.gov/documents/DQ_summaries/CERES_EBAF_Ed4.1_DQS.pdf
#-------------------------------------

se_toa_sw_all, se_toa_sw_clr, se_toa_sw_cre = [2.5, 5.4, 5.9]
se_toa_lw_all, se_toa_lw_clr, se_toa_lw_cre = [2.5, 4.6, 4.5]
se_toa_net_all, se_toa_net_clr, se_toa_net_cre = [3.5, 7.1, 7.4]

se_sfc_lwd_all, se_sfc_lwd_clr, se_sfc_lwd_cre = [9, 8, 9]
se_sfc_lwu_all, se_sfc_lwu_clr, se_sfc_lwu_cre = [15, 15, 17]
se_sfc_lwn_all, se_sfc_lwn_clr, se_sfc_lwn_cre = [17, 17, 18]
se_sfc_swd_all, se_sfc_swd_clr, se_sfc_swd_cre = [14, 6, 14]
se_sfc_swu_all, se_sfc_swu_clr, se_sfc_swu_cre = [11, 11, 14]
se_sfc_swn_all, se_sfc_swn_clr, se_sfc_swn_cre = [13, 13, 16]
se_sfc_net_all, se_sfc_net_clr, se_sfc_net_cre = [20, 21, 26]


#-------------------------------------
# Read data
#-------------------------------------
ceres_data = xr.open_dataset(ceres_path)

# Model variables to consider
model_vars = ['FSUTOA', 'FLUT', 'FLUTC', 'FLNT', 'FLNTC', 'FSNT', 'FSNTC']
A21 = xr.open_mfdataset([noresm_path+var+'_andenes21_20220222_2007-04-15_2010-03-15.nc' for var in model_vars])
M92 = xr.open_mfdataset([noresm_path+var+'_meyers92_20220210_2007-04-15_2010-03-15.nc' for var in model_vars])
#A21 = xr.open_mfdataset([noresm_path+var+'_A21_20240522_2007-04-15_2010-03-15.nc' for var in model_vars])
#M92 = xr.open_mfdataset([noresm_path+var+'_M92_20240522_2007-04-15_2010-03-15.nc' for var in model_vars])

#-------------------------------------
# Compute Arctic average
#-------------------------------------
ceres_Aavg = computeWeightedMean(ceres_data.sel(lat=slice(66.5,90)))
A21_Aavg = computeWeightedMean(A21.sel(lat=slice(66.5,90)))
M92_Aavg = computeWeightedMean(M92.sel(lat=slice(66.5,90)))


#-------------------------------------
# Plot TOA fluxes
#-------------------------------------

print(ceres_Aavg.time)
print(A21.time)

quit()

# Outgoing longwave allsky
plt.figure(figsize=[13,4])
plt.plot(ceres_Aavg.time, ceres_Aavg['toa_lw_all_mon'], label='CERES', color='black')
plt.fill_between(ceres_Aavg.time, ceres_Aavg['toa_lw_all_mon']-se_toa_lw_all, ceres_Aavg['toa_lw_all_mon']+se_toa_lw_all, color='black', alpha=0.1)
plt.plot(M92.time, M92_Aavg['FLUT'], label='M92', color='tab:blue', linestyle='--')
plt.plot(A21.time, A21_Aavg['FLUT'], label='A21', color='tab:orange')
plt.legend(loc="upper right")
plt.xticks(rotation=45, ha='right')
plt.ylabel(r'W/m$^2$')
plt.grid(alpha=0.5)
plt.savefig(fig_path+'pdf/lw_all.pdf', bbox_inches="tight")
plt.savefig(fig_path+'png/lw_all.png', bbox_inches="tight")
plt.clf()


# Outgoing longwave clouds
plt.figure(figsize=[12,4])
plt.plot(ceres_Aavg.time, ceres_Aavg['toa_lw_all_mon'] - ceres_Aavg['toa_lw_clr_c_mon'], label='CERES', color='black',linewidth=2)
obs = ceres_Aavg['toa_lw_all_mon']- ceres_Aavg['toa_lw_clr_c_mon']
plt.fill_between(ceres_Aavg.time, obs - se_toa_lw_cre, obs + se_toa_lw_cre, color='black', alpha=0.1)
plt.plot(A21.time, (A21_Aavg['FLNT']-A21_Aavg['FLNTC']), label='A21', color='tab:orange',linewidth=2)
plt.plot(M92.time, (M92_Aavg['FLNT'] - M92_Aavg['FLNTC']), label='M92', color='tab:blue', linewidth=2, linestyle='--')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25),ncol=3)
plt.xticks(rotation=45, ha='right')
plt.ylabel(r'W/m$^2$')
plt.grid(alpha=0.5)
plt.savefig(fig_path+'pdf/lw_net_clouds.pdf', bbox_inches="tight")
plt.savefig(fig_path+'png/lw_net_clouds.png', bbox_inches="tight")
plt.clf()


# Net all-sky
plt.figure(figsize=[13,4])
plt.plot(ceres_Aavg.time, ceres_Aavg['toa_net_all_mon'], label='CERES', color='black')
plt.plot(ceres_Aavg.time, ceres_Aavg['toa_net_all_mon']+se_toa_net_all, color='black', linestyle='--')
plt.plot(ceres_Aavg.time, ceres_Aavg['toa_net_all_mon']-se_toa_net_all, color='black', linestyle='--')
plt.plot(M92.time, (M92_Aavg['FSNT']-M92_Aavg['FLNT']), label='M92', color='tab:blue')
plt.plot(A21.time, (A21_Aavg['FSNT']-A21_Aavg['FLNT']), label='A21', color='tab:orange')
plt.legend(loc="upper right")
plt.xticks(rotation=45, ha='right')
plt.ylabel(r'W/m$^2$')
plt.grid(alpha=0.5)
plt.savefig(fig_path+'png/net_all.png', bbox_inches="tight")
plt.savefig(fig_path+'pdf/net_all.pdf', bbox_inches="tight")
plt.clf()


# Net clouds
plt.figure(figsize=[13,4])
plt.plot(ceres_Aavg.time, ceres_Aavg['toa_net_all_mon'] - ceres_Aavg['toa_net_clr_c_mon'], label='CERES', color='black')
plt.plot(ceres_Aavg.time, ceres_Aavg['toa_net_all_mon'] - ceres_Aavg['toa_net_clr_c_mon']+se_toa_net_cre, color='black', linestyle='--')
plt.plot(ceres_Aavg.time, ceres_Aavg['toa_net_all_mon'] - ceres_Aavg['toa_net_clr_c_mon']-se_toa_net_cre, color='black', linestyle='--')
plt.plot(M92.time, ((M92_Aavg['FSNT']-M92_Aavg['FLNT'])- (M92_Aavg['FSNTC']-M92_Aavg['FLNTC'])), label='M92', color='tab:blue')
plt.plot(A21.time, ((A21_Aavg['FSNT']-A21_Aavg['FLNT']) - (A21_Aavg['FSNTC']-A21_Aavg['FLNTC'])), label='A21', color='tab:orange')
plt.legend(loc="upper right")
plt.xticks(rotation=45, ha='right')
plt.ylabel(r'W/m$^2$')
plt.grid(alpha=0.5)
plt.savefig(fig_path+'pdf/net_clouds.pdf', bbox_inches="tight")
plt.savefig(fig_path+'png/net_clouds.png', bbox_inches="tight")
plt.clf()


"""
### SURFACE FLUXES
plt.figure()
plt.suptitle("Surface Net LW Flux")
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_net_lw_all_mon'], label='CERES', color='tab:blue')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_net_lw_all_mon']+se_sfc_lwn_all, color='tab:blue', linestyle='--')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_net_lw_all_mon']-se_sfc_lwn_all, color='tab:blue', linestyle='--')
plt.plot(A21.time, -A21_Aavg['FLNS'], label='A21', color='tab:orange')
plt.plot(M92.time, -M92_Aavg['FLNS'], label='M92', color='tab:green')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.ylabel(r'W/m$^2$')
plt.savefig(fig_path+'sfc_lw.png')

plt.figure()
plt.suptitle("Surface Net LW Flux Clear-sky")
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_net_lw_clr_t_mon'], label='CERES', color='tab:blue')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_net_lw_clr_t_mon']+se_sfc_lwn_all, color='tab:blue', linestyle='--')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_net_lw_clr_t_mon']-se_sfc_lwn_all, color='tab:blue', linestyle='--')
plt.plot(A21.time, -A21_Aavg['FLNSC'], label='A21', color='tab:orange')
plt.plot(M92.time, -M92_Aavg['FLNSC'], label='M92', color='tab:green')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.ylabel(r'W/m$^2$')
plt.savefig(fig_path+'sfc_lw_clr.png')

plt.figure()
plt.suptitle("Surface Net SW Flux")
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_net_sw_all_mon'], label='CERES', color='tab:blue')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_net_sw_all_mon']+se_sfc_swn_all, color='tab:blue', linestyle='--')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_net_sw_all_mon']-se_sfc_swn_all, color='tab:blue', linestyle='--')
plt.plot(A21.time, A21_Aavg['FSNS'], label='A21', color='tab:orange')
plt.plot(M92.time, M92_Aavg['FSNS'], label='M92', color='tab:green')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.ylabel(r'W/m$^2$')
plt.savefig(fig_path+'sfc_sw_cre.png')


plt.figure()
plt.suptitle("Surface Net SW CRE")
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_cre_net_sw_mon'], label='CERES', color='tab:blue')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_cre_net_sw_mon']+se_sfc_swn_cre, color='tab:blue', linestyle='--')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_cre_net_sw_mon']-se_sfc_swn_cre, color='tab:blue', linestyle='--')
plt.plot(A21.time, A21_Aavg['SWCFS'], label='A21', color='tab:orange')
plt.plot(M92.time, M92_Aavg['SWCFS'], label='M92', color='tab:green')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.ylabel(r'W/m$^2$')
plt.savefig(fig_path+'sfc_sw_cre.png')

plt.figure()
plt.suptitle("Surface Net LW CRE")
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_cre_net_lw_mon'], label='CERES', color='tab:blue')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_cre_net_lw_mon']+se_sfc_lwn_cre, color='tab:blue', linestyle='--')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_cre_net_lw_mon']-se_sfc_lwn_cre, color='tab:blue', linestyle='--')
plt.plot(A21.time, A21_Aavg['LWCFS'], label='A21', color='tab:orange')
plt.plot(M92.time, M92_Aavg['LWCFS'], label='M92', color='tab:green')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.ylabel(r'W/m$^2$')
plt.savefig(fig_path+'sfc_lw_cre.png')

plt.figure()
plt.suptitle("Surface Net total CRE")
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_cre_net_tot_mon'], label='CERES', color='tab:blue')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_cre_net_tot_mon']+se_sfc_net_cre, color='tab:blue', linestyle='--')
plt.plot(ceres_Aavg.time, ceres_Aavg['sfc_cre_net_tot_mon']-se_sfc_net_cre, color='tab:blue', linestyle='--')
plt.plot(A21.time, (A21_Aavg['SWCFS']+A21_Aavg['LWCFS']), label='A21', color='tab:orange')
plt.plot(M92.time, (M92_Aavg['SWCFS']+M92_Aavg['LWCFS']), label='M92', color='tab:green')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.ylabel(r'W/m$^2$')
plt.savefig(fig_path+'sfc_tot_cre.png')



### CLOUD CHARACTERISTICS
plt.figure()
plt.suptitle("Total cloud fraction")
plt.plot(ceres_Aavg.time, ceres_Aavg['cldarea_total_daynight_mon'], label='CERES', color='tab:blue')
plt.plot(A21.time, A21_Aavg['CLDTOT']*100, label='A21', color='tab:orange')
plt.plot(M92.time, M92_Aavg['CLDTOT']*100, label='M92', color='tab:green')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.ylabel('%')
plt.savefig(fig_path+'cldfrc_tot.png')

plt.show()
"""
