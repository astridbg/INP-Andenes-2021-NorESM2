import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
# Set font style to match latex document----------
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':20})
# ------------------------------------------------
from functions import *

# CALIPSO-GOCCP DATA
# Data must be downloaded from https://climserv.ipsl.polytechnique.fr/cfmip-obs/Calipso_goccp.html 
homepath = "/home/astridbg/Documents/nird/" # Change to suitable path
homepath = "/projects/NS9600K/astridbg/"

calipso_path = homepath + "observational_data/CALIPSO-GOCCP/"
calipso_path = homepath + "data/observations/CALIPSO-GOCCP/"
model_path=homepath+"model_data/noresm_postprocessed/"

wpath=homepath+"INP-Andenes-2021-NorESM2/figures/"

#-------------------------------------
# Read data
#-------------------------------------
# CALIPSO-GOCCP
filenames = glob.glob(calipso_path +"20*/Map*")
filenames.sort()
calipso_ds = xr.open_mfdataset(filenames, compat='override',coords='all')

# NorESM model data
model_var = 'CLDTOT'
model_vars = [model_var+'_CAL',model_var+'_CAL_ICE',model_var+'_CAL_LIQ', model_var+'_CAL_UN']
A21 = xr.open_mfdataset([model_path+var+'_A21_20240612_2007-04-15_2010-03-15.nc' for var in model_vars])
M92 = xr.open_mfdataset([model_path+var+'_M92_20240612_2007-04-15_2010-03-15.nc' for var in model_vars])

#-------------------------------------
# Compute Arctic average
#-------------------------------------

calipso_ds = calipso_ds.sel(time=slice('2007-04-15','2010-03-16'))
calipso_var = 'cltcalipso'

# Compute weighted Arctic average and group by month
CALIOP_Aavg = computeWeightedMean_CALIOP(calipso_ds[calipso_var].sel(latitude=slice(66.5,82))).groupby("time.month").mean("time")
CALIOP_ICE_Aavg = computeWeightedMean_CALIOP(calipso_ds[calipso_var+'_ice'].sel(latitude=slice(66.5,82))).groupby("time.month").mean("time")
CALIOP_LIQ_Aavg = computeWeightedMean_CALIOP(calipso_ds[calipso_var+'_liq'].sel(latitude=slice(66.5,82))).groupby("time.month").mean("time")
CALIOP_UN_Aavg = computeWeightedMean_CALIOP(calipso_ds[calipso_var+'_un'].sel(latitude=slice(66.5,82))).groupby("time.month").mean("time")
A21_Aavg = computeWeightedMean(A21.sel(lat=slice(66.5,82))).groupby("time.month").mean("time")
M92_Aavg = computeWeightedMean(M92.sel(lat=slice(66.5,82))).groupby("time.month").mean("time")

monthsn = np.arange(1,13,1)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May','Jun','Jul','Aug','Sep','Oct','Nov', 'Dec']

#-------------------------------------
# Plot CLOUD COVER BIAS
#-------------------------------------

plt.figure(figsize=[13,4])
plt.hlines(0, 1,12,linewidth=3.5,color='black')

# Plot total cloud cover

plt.fill_between(CALIOP_Aavg.month[:6], (M92_Aavg[model_var+'_CAL'].values*0.01-CALIOP_Aavg.values)[:6], alpha=0.3,label='M92', color='tab:blue')
plt.fill_between(CALIOP_Aavg.month[:6], (A21_Aavg[model_var+'_CAL'].values*0.01-CALIOP_Aavg.values)[:6], alpha=0.3,label='A21', color='tab:orange')

# Change the order of model experiments to have the highest bias in the back
plt.fill_between(CALIOP_Aavg.month[5:8], (A21_Aavg[model_var+'_CAL'].values*0.01-CALIOP_Aavg.values)[5:8], alpha=0.3, color='tab:orange')
plt.fill_between(CALIOP_Aavg.month[5:8], (M92_Aavg[model_var+'_CAL'].values*0.01-CALIOP_Aavg.values)[5:8], alpha=0.3,color='tab:blue')

plt.fill_between(CALIOP_Aavg.month[7:], (M92_Aavg[model_var+'_CAL'].values*0.01-CALIOP_Aavg.values)[7:], alpha=0.3, color='tab:blue')
plt.fill_between(CALIOP_Aavg.month[7:], (A21_Aavg[model_var+'_CAL'].values*0.01-CALIOP_Aavg.values)[7:], alpha=0.3, color='tab:orange')

# Get legend markers
plt.fill_between([1,2],0,0, alpha=0.3,label="Total cloud",color='black')
plt.plot(1,0,linestyle='--',color='grey',label='Ice Cloud')
plt.plot(1,0,label='Liquid Cloud',color='grey')

plt.plot(CALIOP_Aavg.month, A21_Aavg[model_var+'_CAL_LIQ'].values*0.01-CALIOP_LIQ_Aavg.values, color='tab:orange')
plt.plot(CALIOP_Aavg.month, M92_Aavg[model_var+'_CAL_LIQ'].values*0.01-CALIOP_LIQ_Aavg.values, color='tab:blue')

plt.plot(CALIOP_Aavg.month, A21_Aavg[model_var+'_CAL_ICE'].values*0.01-CALIOP_ICE_Aavg.values, color='tab:orange', linestyle='--')
plt.plot(CALIOP_Aavg.month, M92_Aavg[model_var+'_CAL_ICE'].values*0.01-CALIOP_ICE_Aavg.values, color='tab:blue', linestyle='--')

#plt.plot(CALIOP_Aavg.month, A21_Aavg['CLDTOT_CAL_UN'].values*0.01-CALIOP_UN_Aavg[:,0].values, color='tab:orange', linestyle='-.')
#plt.plot(CALIOP_Aavg.month, M92_Aavg['CLDTOT_CAL_UN'].values*0.01-CALIOP_UN_Aavg[:,0].values, color='tab:blue', linestyle='-.')

plt.xticks(monthsn,months,rotation=45, ha='right')
plt.ylabel('Bias (Model-GOCCP)')
plt.grid(alpha=0.5)

# Shrink current axis by 20%
box = plt.gca().get_position()
plt.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.savefig(wpath+'pdf/'+model_var+'_phase_bias.pdf', bbox_inches="tight")
plt.savefig(wpath+'png/'+model_var+'_phase_bias.png', bbox_inches="tight")
plt.clf()

quit()
