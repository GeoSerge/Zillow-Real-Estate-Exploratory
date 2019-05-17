#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 17:17:43 2018

@author: sergeygulbin
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
#df = dfStr.append(dfNum)
df = dfNum.dropna(axis = 1)
df = df.apply(pd.to_numeric, errors='ignore')
df['mean'] = df.mean(axis = 1)


##READ, ORGANIZE AND APPEND MEAN VALUES OF FINANCIAL INDEXES


DJI = pd.read_csv(os.path.join(zillowdir, 'DJI.csv'), low_memory = False)
SP500 = pd.read_csv(os.path.join(zillowdir, 'S&P500.csv'), low_memory = False)
NASDAQ = pd.read_csv(os.path.join(zillowdir, 'NASDAQ.csv'), low_memory = False)
RUSSELL2000 = pd.read_csv(os.path.join(zillowdir, 'RUSSELL2000.csv'), low_memory = False)

for frame, finIndexName in zip([DJI, SP500, NASDAQ, RUSSELL2000],['DJI', 'S&P500', 'NASDAQ', 'RUSSELL2000']):
    frame.index = pd.to_datetime(frame['Date'])
    frame = frame.groupby(pd.TimeGrouper(freq = 'M')).mean()
    frame = frame.apply(pd.to_numeric, errors='ignore')
    df = df.set_index(frame.index)
    df[finIndexName] = frame['Adj Close']
        
    
##PLOT MEAN SQ FT PRICE WITH FINANCIAL INDEXES


#fig, ax1 = plt.subplots()
#ax1.plot(df.index, df['mean'], color = 'blue')
#ax2 = ax1.twinx()
#ax2.plot(df.index, df['DJI'], color = 'black')
#ax2.plot(df.index, df['S&P500'], color = 'red')
#ax2.plot(df.index, df['NASDAQ'], color = 'green')
#plt.title('Mean price per sq. ft, US')
#ax1.set_ylabel('Sq. ft price, $')
#ax2.legend(loc = 0)
#ax2.annotate('R$^2$ = '+ str(round(pearsonr(df['mean'], df['DJI'])[0],2))+'$^{**}$', xy = (0.82, 0.93), xycoords = 'axes fraction')
#ax2.annotate('R$^2$ = '+ str(round(pearsonr(df['mean'], df['S&P500'])[0],2))+'$^{**}$', xy = (0.82, 0.13), xycoords = 'axes fraction', color = 'red')
#ax2.annotate('R$^2$ = '+ str(round(pearsonr(df['mean'], df['NASDAQ'])[0],2))+'$^{**}$', xy = (0.82, 0.28), xycoords = 'axes fraction', color = 'green')
#plt.savefig('/Users/sergeygulbin/Zillow/Pics&Maps/meanSqFtPrice_vs_FinIndexes.png', dpi = 900)


## PLOT MEAN SQ FT PRICE


fig, ax1 = plt.subplots()
ax1.plot(df.index, df['mean'], color = 'blue')
plt.title('Mean price per sq. ft, US')
ax1.set_ylabel('Sq. ft price, $')
ax1.annotate('mean = '+ str(round(df['mean'].mean()))+'$', xy = (0.73, 0.24), xycoords = 'axes fraction')
ax1.annotate('median = '+ str(round(df['mean'].median()))+'$', xy = (0.73, 0.17), xycoords = 'axes fraction')
ax1.annotate('std = '+ str(round(df['mean'].std()))+'$', xy = (0.73, 0.1), xycoords = 'axes fraction')
plt.savefig('/Users/sergeygulbin/Zillow/Pics&Maps/priceUSA_Plot.png', dpi = 900)


##GROUP BY METRO AREAS


#metro = df.groupby('Metro').mean()
#metro = metro.T
#metro = metro[3:]


##PLOT PRICE FOR EVERY METRO AREA
#PLOT BY PRICE GROUPS!!!

#for i in metro.columns:
#    plt.plot(metro.index, metro[i])
