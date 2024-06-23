"""
Author: Astrid Bragstad Gjelsvik
"""

import numpy as np
import pandas as pd
import glob

homepath="/home/astridbg/Documents/nird/"

path_preproc = homepath+"observational_data/Coriolis_preprocessed/"
wpath = homepath+"observational_data/Coriolis_postprocessed/"
fname = "Coriolis_nucleiT.csv"

# Read in Coriolis freezing temperatures

nucleiT = pd.read_csv(path_preproc+fname)

# Adjust freezing temperatures with calibration values

slope = 0.89
intercept = 0.30

nucleiT_cal = nucleiT.iloc[:,:] * slope + intercept

nucleiT_cal.to_csv(wpath+"Coriolis_nucleiT_cal.csv")


print(np.shape(nucleiT_cal))
