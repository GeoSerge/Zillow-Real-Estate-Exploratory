# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 16:47:19 2017

@author: sgulbin
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats 

zillowdir = '/Users/sergeygulbin/Zillow/Excel'
df = pd.read_csv(os.path.join(zillowdir, 'MedValuePerSqftChangePerYear.csv'), low_memory = False)

## Making histogram of % change/year


#plt.hist(df['change/year%'], bins= 50)
#plt.xlabel('% change/year')
#plt.ylim(ymax = 1300)
#plt.savefig(os.path.join(zillowdir[:-5], 'Pics&Maps/PriceChangeHist.png'), dpi = 900)
#plt.hist(df['change/year$'], bins = 50)
def histShareX(xText, yText, path, *args, **kwargs):
    fig, ax = plt.subplots(len(args), sharex = True)
    for a,b,c,d,e,f in zip(range(len(args)), args, kwargs['binsize'], kwargs['title'], kwargs['showTicks'], kwargs['signs']):
        ax[a].hist(b, bins = c)
        ax[a].set_title(d)
        ax[a].annotate('mean = '+str(round(b.describe()[1], 1))+str(f), xy = (xText,yText), xycoords = 'axes fraction')
        ax[a].annotate('std = '+str(round(b.describe()[2], 1))+str(f), xy = (xText,yText-0.1), xycoords = 'axes fraction')
        ax[a].annotate('median = '+str(round(b.median(), 1))+str(f), xy = (xText, yText-0.2), xycoords = 'axes fraction')
        ax[0].set_xlabel('sq. ft price change per year, $')
        ax[0].set_xlim(xmax = 30)
        ax[1].set_xlabel('sq. ft price change per year, %')
        ax[1].set_xlim(xmax = 30)
        plt.setp(ax[a].get_xticklabels(), visible = e)
        plt.subplots_adjust(hspace = 0.6)
#    plt.savefig(path, dpi = 900)


## Mean price change by state, county, metro


state = df.groupby('State').mean()
state = state['change/year%']
#print state.sort_values(ascending = 0)
#state.to_csv(os.path.join(zillowdir, 'MeanPriceChangeByState.csv'))
county = df.groupby('CountyName').mean()
county = county['change/year%']
#county.to_csv(os.path.join(zillowdir, 'MeanPriceChangeByCounty.csv'))
metro = df.groupby('Metro').mean()
#metro = metro['change/year%']
#print metro.sort_values(ascending = 0)
#metro.to_csv(os.path.join(zillowdir, 'MeanPriceChangeByMetro.csv'))

## Percentile
df['1997PricePercentile'] = 1
df['%changePercentile'] = 2
for i in df.index:
    df.loc[i,'1997PricePercentile'] = stats.percentileofscore(df['1997Price'], df.loc[i,'1997Price'])
    df.loc[i,'2016PricePercentile'] = stats.percentileofscore(df['2016Price'], df.loc[i,'2016Price'])
#    df.loc[i,'%changePercentile'] = stats.percentileofscore(df['change/year%'], df.loc[i,'change/year%'])
df['differ'] = df['2016PricePercentile'] - df['1997PricePercentile']
df.to_csv(os.path.join(zillowdir, 'PercentileDiffByZip.csv'))

def scatterFittedLine(x,y, xlabel, ylabel, path):
    m,b = np.polyfit(x,y,1)    
    plt.scatter(x,y)
    plt.plot(x, m*x+b, color = 'red')
    if stats.pearsonr(x,y)[1]<=0.01:
        plt.annotate('r  = '+str(round(stats.pearsonr(x,y)[0], 2))+'$^{**}$', xy = (max(x),max(m*x+b)), fontsize = 12)
    if stats.pearsonr(x,y)[1]>0.01 and stats.pearsonr(x,y)[1]<= 0.05:
        plt.annotate('r  = '+str(round(stats.pearsonr(x,y)[0], 2))+'$^*$', xy = (max(x),max(m*x+b)), fontsize = 12)
    if stats.pearsonr(x,y)[1]> 0.05:
        plt.annotate('r  = '+str(round(stats.pearsonr(x,y)[0], 2)), xy = (max(x),max(m*x+b)), fontsize = 12)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
#    plt.savefig(path, dpi = 900)

    
