import xarray as xr
import pandas as pd
import numpy as np
import glob
import functions


rpath="../../model_data/noresm_output/"
wpath="../../model_data/noresm_postprocessed/"


# Choose which case to postprocess

case = "M92_20241122" # Baseline case with Meyers' parameterisation
#case = "A21_20241125" # Andenes 2021 INP parameterisation

casefolder="NF2000climo_f19_tn14_"+case

all_files = glob.glob(rpath+casefolder+"/atm/hist/"+casefolder+".cam.h0.*")
all_files.sort()
print("Files found")

ds = xr.open_mfdataset(all_files)
print("Dataset created")

#-----------------------------
# Postprocessing of model data
#-----------------------------

print(ds.time)

# Fix timestamp of model data
ds = functions.fix_cam_time(ds)

# Remove spinup months of data set
ds = ds.isel(time=slice(3,len(ds.time)))

#-----------------------------

print("Postprocessing completed")

#--------------------------------------------------------------------
# Store relevant variables intermediately to save time when plotting,
# change to desired units and create combined variables 
#--------------------------------------------------------------------
date = "2007-04-15_2010-03-15"

variables = ["OCNFRAC","FREQI","NUMICE","LWCFS","SWCFS","NETCFS","CLOUD","CLDTOT", "TGCLDTWP","TREFHT", "PREC", "CLDLWEMS",
             "FSNT","FSNTC","FLNT", "FLNTC", "FSNS", "FLNS", "CLDTOT_CAL", "CLDTOT_CAL_ICE", "CLDTOT_CAL_LIQ", "CLDTOT_CAL_UN",
             "TGCLDIWP","TGCLDLWP"] # These last two must be placed last, before TGCLTWP and CLDLEWMS

for var in variables:
    print("Started writing variable:")
	
    # Change to desired units

    if var == "TREFHT":
        ds[var].values = ds[var].values - 273.15 # Change unit to degrees Celsius
        ds[var].attrs["units"] = r"$^{\circ}$C"
	
    if var == "TGCLDIWP" or var == "TGCLDLWP":
        ds[var].values = ds[var].values*1e+3 # Change unit to grams per squared meter
        ds[var].attrs["units"] = "g/m$^2$"

    # Make combined data variables
    if var == "TGCLDTWP":
        ds = ds.assign(TGCLDTWP=ds["TGCLDIWP"]+ds["TGCLDLWP"])
        if "TGCLDIWP" or "TGCLDLWP" not in variables:
            ds[var].values = ds[var].values*1e+3 # Change unit to grams per squared meter
            ds[var].attrs["units"] = "g/m$^2$"
        ds[var].attrs["long_name"] = "Total Grid-box Cloud Total Water Path"

    if var == "LWCFS":
        ds = ds.assign(LWCFS=ds["FLNSC"]-ds["FLNS"])
        ds[var].attrs["units"] = "W/m$^2$"
        ds[var].attrs["long_name"] = "Longwave cloud radiative effect at surface"

    if var == "SWCFS":
        ds = ds.assign(SWCFS=ds["FSNS"]-ds["FSNSC"])
        ds[var].attrs["units"] = "W/m$^2$"
        ds[var].attrs["long_name"] = "Shortwave cloud radiative effect at surface"
	        
    if var == "NETCFS":
        ds = ds.assign(NETCFS=ds["FSNS"]-ds["FSNSC"]-ds["FLNS"]-(-ds["FLNSC"]))
        ds[var].attrs["units"] = "W/m$^2$"
        ds[var].attrs["long_name"] = "Net cloud radiative effect at surface"

    if var == "CLDLWEMS":
        ds = ds.assign(CLDLWEMS=1-np.exp(-0.158*ds["TGCLDLWP"]*1e+3))
        ds[var].attrs["units"] = "Emissivity"
        ds[var].attrs["long_name"] = "Cloud Longwave Emissivity"
    
    if var == "PREC":
        print(ds["PRECL"].attrs["units"])
        print(ds["PRECC"].attrs["units"])
        print("NB! Changing units to mm/month!")
        ds = ds.assign(PREC=(ds["PRECL"]+ds["PRECL"])*1e+3*60*60*24*30) # Sum precipitation rates
        ds[var].attrs["units"] = "mm/month" # Change unit to millimeter per month
        ds[var].attrs["long_name"] = "Total Precipitation"
    
    print(ds[var].attrs["long_name"])
    print("Units: ", ds[var].attrs["units"])
	
    ds[var].to_netcdf(wpath+var+"_"+case+"_"+date+".nc")
