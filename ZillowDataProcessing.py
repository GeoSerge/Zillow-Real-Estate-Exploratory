# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 11:45:28 2017

@author: sgulbin
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

##Basic dataframe conversion


zillowdir = 'E:/my_projects/Zillow/Excel'
df = pd.read_csv(os.path.join(zillowdir, 'Zip_MedianValuePerSqft_AllHomes.csv'), low_memory = False)
df = df.T
#df.columns = df.loc['RegionName']


##Adding datetime index


lst = []
for i in pd.date_range('4/1/1996','7/1/2017', freq='MS'):
    lst.append(i)
df.index = df.index.tolist()[:7]+lst
df.replace('', np.nan)


##Leaving only 20-year period records (1997 - 2016)


dfStr = df.iloc[:7]
dfNum = df.iloc[8:]
dfNum = dfNum[dfNum.index > pd.to_datetime('12/31/1996')]
dfNum = dfNum[dfNum.index < pd.to_datetime('1/1/2017')]
df = dfStr.append(dfNum)
df = df.dropna(axis = 1) ##Deleting records with period of observations smaller than 20 years


df = df.apply(pd.to_numeric, errors='ignore')
df.loc['1997Price'] = 1
df.loc['2016Price'] = 2
df.loc['diff$'] = 3
df.loc['diff%'] = 4
df.loc['change/year$'] = 5
df.loc['change/year%'] = 6
for i in df.columns:
    df.loc['1997Price'][i] = df[i][7]
    df.loc['2016Price'][i] = df[i][-7]
    df.loc['diff$'][i] = df.loc['2016Price'][i] - df.loc['1997Price'][i]
    df.loc['diff%'][i] = (df.loc['2016Price'][i] - df.loc['1997Price'][i])*100/df.loc['1997Price'][i]
    df.loc['change/year$'][i] = (df[i].loc['diff$']/20)
    df.loc['change/year%'][i] = (df[i].loc['diff%']/20)
df1 = df.iloc[:7]
df2 = df.iloc[-6:]
df = df1.append(df2, ignore_index = True)
df = df.T
df = df.reset_index(drop = True)
df.columns = ['RegionID', 'ZIPcode', 'City', 'State', 'Metro', 'CountyName', 'SizeRank', '1997Price', '2016Price', 'diff$','diff%', 'change/year$', 'change/year%'] 
df.to_csv(os.path.join(zillowdir, 'MedValuePerSqftChangePerYear.csv')) 
print df.sort_values(by = 'change/year%', ascending = 0).reset_index(drop = True).loc[0]
print df.sort_values(by = 'change/year%', ascending = 1).reset_index(drop = True).loc[0]