#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 16:00:20 2018

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
dfNum = dfNum[dfNum.index == pd.to_datetime('07/01/2017')]
dfNum = dfNum.apply(pd.to_numeric, errors='ignore')


##GROUP BY METRO AREAS


df = dfStr.loc[['Metro', 'State', 'RegionName']].append(dfNum)
df = df.dropna(axis = 1)
dfT = df.T
dfT.to_csv(os.path.join(zillowdir, '2017.csv'))