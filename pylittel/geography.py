# -*- coding: utf-8 -*-

"""
LitTEL

@name:     geography.py
@date:     26/06/2023
@author:   Reuben J. Pitts

This script visualises a map using a TimeSlice

"""

### 0 ### Imports

# littel imports
from littel.functions import get_code, get_date, get_feature
from littel.timeslice import TimeSlice

# library imports
import pandas as pd

# matplotlib and cartopy imports
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.markers import MarkerStyle
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# set some matplotlib parametres
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['savefig.facecolor'] ='white'
plt.rcParams["figure.figsize"] = (20,20)


### 1 ### Create a map

def geography(date, feat):
    
    # get a TimeSlice
    ts = TimeSlice(date, feat)
        
    # create a map
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree())

    # set the outlines of the map
    ax.coastlines()
    ax.add_feature(cfeature.OCEAN, zorder=0, edgecolor="white")
    ax.add_feature(cfeature.LAND, zorder=0, edgecolor="white")
    ax.set_extent((-10, 50, 10, 60))
    
    # create the scatter
    for i in [0, 1]:
        ax.scatter(ts.longitude(subset=i),
                   ts.latitude(subset=i),
                   s = 250,
                   linewidth = 2,
                   edgecolor = 'black',
                   zorder = 1,
                   label = get_code(feat, i))
    
    # deal with 'both'
    ax.scatter(ts.longitude(subset=0.5),
               ts.latitude(subset=0.5),
               s = 250,
               c = '#ff7f0e',
               linewidth = 2,
               edgecolor = 'black',
               zorder = 1)
    
    ax.scatter(ts.longitude(subset=0.5),
               ts.latitude(subset=0.5),
               s = 150,
               marker=MarkerStyle('o', fillstyle='left'),
               c='#1f77b4',
               zorder=2)

    # add text
    for lon, lat, n in ts.labels():
        if not pd.isna(lon) and not pd.isna(lat):
            ax.text(lon + 0.5, lat, n, fontsize=20)
        
    # add a legend
    ax.legend(prop={'size': 24})
    
    # add a title
    ax.set_title(get_feature(feat) + ': map for ' + get_date(date), fontsize=30)

    
