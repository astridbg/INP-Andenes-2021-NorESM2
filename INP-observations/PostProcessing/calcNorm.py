# Author: Tim Carlsen
# Modified by: Astrid Bragstad Gjelsvik

import numpy as np
import pandas as pd
import xarray as xr
import glob

homepath="/home/astridbg/Documents/nird/"

path_data = homepath+"observational_data/"
path_preproc = homepath+"observational_data/Coriolis_preprocessed/"
path_surface_pressure = homepath+"observational_data/SN87110/"
path_temp = homepath+"observational_data/Inlet_Temp/"
wpath = homepath+"observational_data/Coriolis_postprocessed/"

# Read in Coriolis INP concentrations

nucleiOut = pd.read_csv(path_preproc+"Coriolis_nucleiOut.csv")
nCor = len(nucleiOut.iloc[0,:])

# Read in Coriolis log file

df_cor = pd.read_csv(path_data+"coriolis_log_all.csv", skiprows = 1)

t_start = pd.DataFrame(df_cor['Date'] + ' ' + df_cor['Start (UTC)'], columns = ['t_start'])
t_start = t_start.set_index('t_start')
t_start.index = pd.to_datetime(t_start.index, format = '%d-%m-%Y %H:%M')

t_end = pd.DataFrame(df_cor['Date'] + ' ' + df_cor['End (UTC)'], columns = ['t_end'])
t_end = t_end.set_index('t_end')
t_end.index = pd.to_datetime(t_end.index, format = '%d-%m-%Y %H:%M')

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

# Get pressure data

ds_pres = xr.open_dataset(path_surface_pressure+"air_pressure_at_sea_level_202103.nc")
df_pres = ds_pres.to_dataframe()

# Create lists for average pressures and temperatures

pres_all = []
temp_all = []

i = 1
for cor in t_start.index:

    print(cor.date(),", Coriolis sample: ",i)
    
    # Average over Coriolis sampling time periods

    time_pres = df_pres[str(cor.date())].index.hour
    index_cor_pres = np.where(np.logical_or(time_pres == cor.hour, time_pres == int(cor.hour + cor.minute/60. + 40./60.)))
    pres = np.nanmean(np.array(df_pres['air_pressure_at_sea_level'][str(cor.date())])[index_cor_pres])
    
    time_temp = df_temp[str(cor.date())].index.hour + df_temp[str(cor.date())].index.minute/60. + df_temp[str(cor.date())].index.second/3600.
    
    index_cor_temp = np.where((time_temp >= cor.hour+cor.minute/60.) & (time_temp <= cor.hour + cor.minute/60. + 40./60.))
    
    temp = np.nanmean(np.array(df_temp['Temperature(C)'][str(cor.date())])[index_cor_temp])
    
    # Add average pressure and temperature to the list 
    
    pres_all = np.append(pres_all, pres)
    temp_all = np.append(temp_all, temp)
    i += 1


# Convert INP concentrations per litre to per standard litre

nucleiOut_std = nucleiOut
p_std = 1013.25
T_std = 273.15

for cor in range(nCor):
    
    nucleiOut_std.iloc[:,cor] = nucleiOut.iloc[:,cor] * p_std/pres_all[cor] * (273.15 + temp_all[cor])/T_std 
    #nucleiOut_std.iloc[:,cor] = nucleiOut.iloc[:,cor] * pres_all[cor]/p_std * T_std/(273.15 + temp_all[cor])
nucleiOut_std.to_csv(wpath+"Coriolis_nucleiOut_std.csv")
print(np.shape(nucleiOut_std))


