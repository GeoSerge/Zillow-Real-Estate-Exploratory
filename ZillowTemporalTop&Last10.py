# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 17:22:32 2017

@author: sgulbin
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr

zillowdir = '/Users/sergeygulbin/Zillow/Excel'
df = pd.read_csv(os.path.join(zillowdir, 'Zip_MedianValuePerSqft_AllHomes.csv'), low_memory = False)
df = df.T

    
##ADDING DATETIME INDEX


lst = []
for i in pd.date_range('4/1/1996','7/1/2017', freq='MS'):
    lst.append(i)
df.index = df.index.tolist()[:7]+lst
df.replace('', np.nan)


##LEAVING ONLY 20-YEAR PERIOD RECORDS (1997-2016)


dfStr = df.iloc[:7]
dfNum = df.iloc[8:]
dfNum = dfNum[dfNum.index > pd.to_datetime('12/31/1996')]
dfNum = dfNum[dfNum.index < pd.to_datetime('1/1/2017')]
dfNum = dfNum.apply(pd.to_numeric, errors='ignore')


##GROUP BY METRO AREAS


df = dfStr.loc[['Metro', 'State']].append(dfNum)
df = df.dropna(axis = 1)
dfT = df.T
dfT.index = dfT['Metro']
grouped = dfT.groupby(dfT.index).apply(lambda x: x.sum()) #ADDING STATES COLUMN TO THE GROUPED DATA FRAME. BECAUSE NO STRING DATA SHOULD BE IN A DATAFRAME THAT IS BEING GROUPED
states = []
for i in grouped['State']:
    states.append(i[:2])
dfT = dfT.iloc[:, 2:]
dfT = dfT.apply(pd.to_numeric, errors='ignore')
metro = dfT.groupby(dfT.index).mean()
metro['State'] = states
metro['mean'] = metro.mean(axis = 1)
metro_sorted = metro.sort_values(by = 'mean', ascending = 0)
metroTop10 = metro_sorted.iloc[:10, :-2]
metroTop10['State'] = metro_sorted.iloc[:10, :]['State']
metroTop10.index = metroTop10.index+', '+metroTop10['State']
metroTop10 = metroTop10.iloc[:,:-1]
metroLast10 = metro_sorted.iloc[-10:, :-2]
metroLast10['State'] = metro_sorted.iloc[-10:, :]['State']
metroLast10.index = metroLast10.index+', '+metroLast10['State']
metroLast10 = metroLast10.iloc[:, :-1]
metroTop10 = metroTop10.T
metroLast10 = metroLast10.T


##GROUP BY STATES


dfStates = dfStr.loc[['State']].append(dfNum)
dfStates = dfStates.dropna(axis = 1)
dfT_States = dfStates.T
dfT_States.index = dfT_States['State']
dfT_States = dfT_States.iloc[:, 1:]
dfT_States = dfT_States.apply(pd.to_numeric, errors='ignore')
states = dfT_States.groupby(dfT_States.index).mean()
states['mean'] = states.mean(axis = 1)
statesSorted = states.sort_values(by = 'mean', ascending = 0)
statesTop10 = statesSorted.iloc[:10, :-1].T
statesLast10 = statesSorted.iloc[-10:, :-1].T
statesT = statesSorted.iloc[-39:, :-1].T


##PLOT PRICE FOR 10 MOST AND LEAST EXPENSIVE METRO AREAS


metroTop10.plot(colormap = 'spectral', linewidth = 2)
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.ylabel('sq. ft price, $')
#plt.savefig('/Users/sergeygulbin/Zillow/Pics&Maps/TemporalTop10Metro.png', dpi = 900,bbox_inches='tight')
metroLast10.plot(colormap = 'spectral', linewidth = 2)
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.ylabel('sq. ft price, $')
#plt.savefig('/Users/sergeygulbin/Zillow/Pics&Maps/TemporalLast10Metro.png', dpi = 900,bbox_inches='tight')


##PLOT PRICE FORT 10 MOST AND LEAST EXPENSIVE STATES


statesTop10.plot(colormap = 'spectral', linewidth = 2)
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.ylabel('sq. ft price, $')
#plt.savefig('/Users/sergeygulbin/Zillow/Pics&Maps/TemporalTop10States.png', dpi = 900,bbox_inches='tight')
statesLast10.plot(colormap = 'spectral', linewidth = 2)
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.ylabel('sq. ft price, $')
#plt.savefig('/Users/sergeygulbin/Zillow/Pics&Maps/TemporalLast10States.png', dpi = 900,bbox_inches='tight')
statesT.plot(colormap = 'spectral', linewidth = 2)
plt.legend(loc = 'upper center', bbox_to_anchor = (0.5, -0.1), ncol = 5)
plt.ylabel('sq. ft price, $')
#plt.savefig('/Users/sergeygulbin/Zillow/Pics&Maps/TemporalAllStates.png', dpi = 900,bbox_inches='tight')