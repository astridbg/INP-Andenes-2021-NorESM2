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
model_vars = ['FLNT', 'FLNTC', 'FSNT', 'FSNTC']
A21 = xr.open_mfdataset([noresm_path+var+'_A21_20240612_2007-04-15_2010-03-15.nc' for var in model_vars])
M92 = xr.open_mfdataset([noresm_path+var+'_M92_20240612_2007-04-15_2010-03-15.nc' for var in model_vars])


#-------------------------------------
# Plot TOA fluxes

# Compute Arctic+monthly average
#-------------------------------------

ceres_Aavg = computeWeightedMean(ceres_data.sel(lat=slice(66.5,90))).groupby("time.month").mean("time")
A21_Aavg = computeWeightedMean(A21.sel(lat=slice(66.5,90))).groupby("time.month").mean("time")
M92_Aavg = computeWeightedMean(M92.sel(lat=slice(66.5,90))).groupby("time.month").mean("time")

monthsn = np.arange(1,13,1)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May','Jun','Jul','Aug','Sep','Oct','Nov', 'Dec']

fig, [ax1, ax2] = plt.subplots(2, 1, sharex=True, figsize=[12,8])

# Outgoing longwave clouds
obs1 = ceres_Aavg['toa_lw_all_mon']- ceres_Aavg['toa_lw_clr_c_mon']
ax1.plot(ceres_Aavg.month, obs1, label='CERES', color='black',linewidth=2)
ax1.fill_between(ceres_Aavg.month, obs1 - se_toa_lw_cre, obs1 + se_toa_lw_cre, color='black', alpha=0.1)
ax1.plot(A21_Aavg.month, (A21_Aavg['FLNT']-A21_Aavg['FLNTC']), label='A21', color='tab:orange',linewidth=2)
ax1.plot(M92_Aavg.month, (M92_Aavg['FLNT'] - M92_Aavg['FLNTC']), label='M92', color='tab:blue', linewidth=2, linestyle='--')
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25),ncol=3)
#ax1.set_xticks(monthsn, months, rotation=45, ha='right')
ax1.set_ylabel(r'W/m$^2$')
ax1.grid(alpha=0.5)
ax1.annotate('(a)',fontsize=20,
        xy=(0, 1), xycoords='axes fraction',
        xytext=(-30, 30), textcoords='offset points',
        ha='left', va='top')

# Net (outgoing) shortwave clouds
obs2 = (ceres_Aavg['solar_mon']-ceres_Aavg['toa_sw_all_mon']) - (ceres_Aavg['solar_mon']-ceres_Aavg['toa_sw_clr_c_mon'])
ax2.plot(ceres_Aavg.month, -obs2, label='CERES', color='black',linewidth=2)
ax2.fill_between(ceres_Aavg.month, -obs2 - se_toa_sw_cre, -obs2 + se_toa_sw_cre, color='black', alpha=0.1)
ax2.plot(A21_Aavg.month, -(A21_Aavg['FSNT']-A21_Aavg['FSNTC']), label='A21', color='tab:orange',linewidth=2)
ax2.plot(M92_Aavg.month, -(M92_Aavg['FSNT'] - M92_Aavg['FSNTC']), label='M92', color='tab:blue', linewidth=2, linestyle='--')
ax2.set_xticks(monthsn, months,rotation=45, ha='right')
ax2.set_ylabel(r'W/m$^2$')
ax2.grid(alpha=0.5)
ax2.annotate('(b)',fontsize=20,
        xy=(0, 1), xycoords='axes fraction',
        xytext=(-30, 30), textcoords='offset points',
        ha='left', va='top')

fig.savefig(fig_path+'pdf/lw_sw_net_clouds_monthly.pdf', bbox_inches="tight")
fig.savefig(fig_path+'png/lw_sw_net_clouds_monthly.png', bbox_inches="tight")
plt.clf()