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


model_rpath="../../model_data/noresm_postprocessed/"
obs_rpath="../../observational_data/radiation/stations/" # Data must be downloaded from https://pangaea.de
obs_rpath="../../data/observations/radiation/stations/" # Data must be downloaded from https://pangaea.de
wpath="../figures/"

station_paths = ["ALE_basic_rad_2004-2014/datasets/ALE_basic_rad_2004-2014.csv",
                 "BAR_radiation_1992-01_etseq/datasets/BAR_radiation_1992-2022.csv",
                 "NYA_radiation_2006-05_etseq/datasets/NYA_radiation_2006-2023.csv"]

#-------------------------------------
# Station coordinates and names
#-------------------------------------

ALE_lat = 82.5; ALE_lon = 360-62.3
NYA_lat = 78.9227; NYA_lon = 11.927300
BAR_lat = 71.17; BAR_lon = 360-156.47

station_coords = [[ALE_lat, ALE_lon], 
                  [BAR_lat, BAR_lon], 
                  [NYA_lat, NYA_lon]]
station_names = ["Alert", "Utqiaġvik", "Ny-Ålesund"]
#-------------------------------------
# Read data
#-------------------------------------

obs_dfs = []
for i in range(len(station_paths)):
    df = pd.read_csv(obs_rpath+station_paths[i], index_col=0)
    obs_dfs.append(df)

# Model variables to consider
model_vars = ['FSNS', 'FLNS']
A21 = xr.open_mfdataset([model_rpath+var+'_A21_20241125_2007-04-15_2010-03-15.nc' for var in model_vars])
M92 = xr.open_mfdataset([model_rpath+var+'_M92_20241122_2007-04-15_2010-03-15.nc' for var in model_vars])

#-------------------------------------
# Three subplots in one
# Monthly averages
#-------------------------------------

A21_month = A21.groupby("time.month").mean("time")
M92_month = M92.groupby("time.month").mean("time")

obs = obs_dfs[0].loc["2007-04":"2010-03"]
obs.index = pd.to_datetime(obs.index)

monthsn = np.arange(1,13,1)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May','Jun','Jul','Aug','Sep','Oct','Nov', 'Dec']

# Net Surface Flux
labels = ['(a)', '(b)', '(c)']
fig, axs = plt.subplots(3, 1, sharex=True, figsize=[13,12])
for i, df, coord, name, label in zip(range(3), obs_dfs, station_coords, station_names, labels): 
    #Plot observations
    df = df.loc["2007-04":"2010-03"]
    df.index = pd.to_datetime(df.index)
    df = df.groupby(df.index.month).mean()
    obs = (df['SWD [W/m**2]'] + df['LWD [W/m**2]'] - df['SWU [W/m**2]'] - df['LWU [W/m**2]'])
    obs.plot(label='Observed', color='black', ax=axs[i], linewidth=2)
    #Plot uncertainty
    axs[i].fill_between(np.arange(1,13,1), obs - obs*(0.095), obs + obs*(0.095), color='black', alpha=0.1)
    #Plot model
    axs[i].plot(np.arange(1,13,1),(A21_month['FSNS'] - A21_month['FLNS']).sel(lat=coord[0], lon=coord[1], method='nearest'), label='A21', color='tab:orange', linewidth=2 )
    axs[i].plot(np.arange(1,13,1),(M92_month['FSNS'] - M92_month['FLNS']).sel(lat=coord[0], lon=coord[1], method='nearest'), label='M92', color='tab:blue',linewidth=2, linestyle='--' )
    axs[i].set_title(name)
    if i==0:
        axs[i].legend(loc='upper center', bbox_to_anchor=(0.5, 1.45),ncol=3)
    axs[i].annotate(label,fontsize=20,
        xy=(0, 1), xycoords='axes fraction',
        xytext=(-30, 30), textcoords='offset points',
        ha='left', va='top')
    axs[i].set_ylabel(r'W/m$^2$')
    axs[i].set_ylim([-55,160])
    axs[i].set_xlabel('')
    axs[i].set_xticks(np.arange(1, 13, 1),months)
    axs[i].grid(alpha=0.5)
    axs[i].tick_params('x',labelrotation=45)

fig.savefig(wpath+'pdf/stations_all_net_monthly.pdf', bbox_inches="tight")
fig.savefig(wpath+'png/stations_all_net_monthly.png', bbox_inches="tight")

plt.clf()
