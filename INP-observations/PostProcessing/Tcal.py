import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from sklearn.linear_model import LinearRegression
from scipy import interpolate, stats
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':17})

import seaborn as sns

homepath='/home/astridbg/Documents/nird/'

drincopath=homepath+'observational_data/Temp_Calibration/DRINCO_TCal/'
foldernames=['20210327_UpperRight','20210327_BottomRight','20210328_BottomLeft','20210328_UpperLeft','20210329_Center']
cornernames=['Upper right corner','Bottom right corner','Bottom left corner','Upper left corner','Center']
thermopath=homepath+'observational_data/Temp_Calibration/Chiller_Temp_Calib/Temp_Calib_'
filenames=['2021-03-27_13-08-23_bottom_right_and_upper_right','2021-03-27_13-08-23_bottom_right_and_upper_right',
            '2021-03-28_13-44-00_bottom_left_upper_left','2021-03-28_13-44-00_bottom_left_upper_left',
            '2021-03-29_08-54-35']
wpath=homepath+"INP-Andenes-2021-NorESM2/figures/"

colors = sns.color_palette('deep',5)
markers = ['x','o','*','+','^']

plt.figure(figsize=(8,6),dpi=300)

plt.title('Temperature calibration for tray wells')
plt.xlabel(r'DRINCO temperature [$^{\circ}$C]')
plt.ylabel(r'Measured temperature [$^{\circ}$C]')

X = np.array([])
Y = np.array([])

for f in range(len(foldernames)):
    TC=pd.read_csv(thermopath+filenames[f]+'.txt', usecols=[1,2],header=1)
    DR1=pd.read_csv(drincopath+foldernames[f]+'/ramp_1.txt', header=0)
    DR2=pd.read_csv(drincopath+foldernames[f]+'/ramp_2.txt', header=0)
    DR3=pd.read_csv(drincopath+foldernames[f]+'/ramp_3.txt', header=0)

    for i in range(len(DR1.index)):
         DR1.iloc[i,0] = dt.datetime.strptime(DR1.iloc[i,0], '%d-%b-%Y %H:%M:%S')
    for i in range(len(DR2.index)):
        DR2.iloc[i,0] = dt.datetime.strptime(DR2.iloc[i,0], '%d-%b-%Y %H:%M:%S')
    for i in range(len(DR3.index)):
         DR3.iloc[i,0] = dt.datetime.strptime(DR3.iloc[i,0], '%d-%b-%Y %H:%M:%S')
    for i in range(len(TC.index)):
        TC.iloc[i,0] = dt.datetime.strptime(TC.iloc[i,0], '%Y-%m-%d %H:%M:%S')

    TC = TC.rename(columns={TC.columns[0]:"time", TC.columns[1]:"temp_degC"})
    DR1.index = DR1.iloc[:,0]
    DR2.index = DR2.iloc[:,0]
    DR3.index = DR3.iloc[:,0]
    TC.index = TC.iloc[:,0]
    del DR1['time'], DR2['time'], DR3['time'], TC['time']

    DR1_interpol=DR1.resample('5S').mean()
    DR2_interpol=DR2.resample('5S').mean()
    DR3_interpol=DR3.resample('5S').mean()
    TC_interpol=TC.resample('5S').mean()

    DR1_interpol['temp_degC'] = DR1_interpol['temp_degC'].interpolate(method='linear')
    DR2_interpol['temp_degC'] = DR2_interpol['temp_degC'].interpolate(method='linear')
    DR3_interpol['temp_degC'] = DR3_interpol['temp_degC'].interpolate(method='linear')
    TC_interpol['temp_degC'] = TC_interpol['temp_degC'].interpolate(method='linear')

    TC_interpol1=TC_interpol.loc[DR1_interpol.index[0]:DR1_interpol.index[-1]]
    TC_interpol2=TC_interpol.loc[DR2_interpol.index[0]:DR2_interpol.index[-1]]
    TC_interpol3=TC_interpol.loc[DR3_interpol.index[0]:DR3_interpol.index[-1]]

    X = np.append(X,DR1_interpol['temp_degC'])
    X = np.append(X,DR2_interpol['temp_degC'])
    X = np.append(X,DR3_interpol['temp_degC'])

    Y = np.append(Y,TC_interpol1['temp_degC'])
    Y = np.append(Y,TC_interpol2['temp_degC'])
    Y = np.append(Y,TC_interpol3['temp_degC'])

    plt.scatter(DR1_interpol['temp_degC'][::10], TC_interpol1['temp_degC'][::10],marker=markers[f],color=colors[f],label=cornernames[f])
    plt.scatter(DR2_interpol['temp_degC'][::10], TC_interpol2['temp_degC'][::10],marker=markers[f],color=colors[f])
    plt.scatter(DR3_interpol['temp_degC'][::10], TC_interpol3['temp_degC'][::10],marker=markers[f],color=colors[f])


X = X.reshape((-1,1))


linreg = LinearRegression().fit(X,Y)
slope = linreg.coef_[0]
intercept = linreg.intercept_
r2_score = linreg.score(X,Y)

print("intercept:", intercept)
print("slope:", slope)
print("R-squared score:", r2_score)


plt.plot(DR1_interpol['temp_degC'], slope*DR1_interpol['temp_degC'] + intercept, color='black',
        label=r'%.2f + %.2f$\times T_{DRINCO}$' %(intercept, slope))
plt.grid(alpha=0.5)
plt.legend()
plt.savefig(wpath+"Tcal.png", bbox_inches="tight")
