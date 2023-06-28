# -*- coding: utf-8 -*-

"""
LitTEL

@name:     changelog.py
@date:     26/06/2023
@author:   Reuben J. Pitts

This script defines a ChangeLog

A ChangeLog object provides information by a FEATURE and a DIRECTIONALITY
- A feature is expressed as a Feature_ID (e.g. 'Pos_Coord')
- A directionality is expressed as 0 (descending) or 1 (ascending)

"""

### 0 ### Imports

# littel imports
from littel.timelineage import TimeLineage
from littel.functions import get_values

# library imports
import pandas as pd
import numpy as np


### 1 ### Define the ChangeLog class

class ChangeLog:
    
    # initialise the ChangeLog
    def __init__(self, feat, drct):
        self.df = get_values(feat=feat)
        self.languages = list(set(self.df['Language_ID']))
        
        self.feat = feat
        self.directionality = drct
        
        self.duration = 0
        self.increments = []
        self.opposite = []
        self.dates = []
        self.correlations = {}
        
        for l in self.languages:
            tl = TimeLineage(l)
            self.duration += tl.range
            self.dates += tl.change(feat, drct)
            self.increments += tl.increments(feat, drct=drct)
            self.opposite += tl.increments(feat, drct=abs(drct-1))
            for key, value in tl.change_correlations(feat, drct):
                current = self.correlations.get(key,[])
                current.append(value)
                self.correlations[key] = current    
        
    # get average date of changes in the ChangeLog
    def average_date(self):
        return np.mean(self.dates)
        
    # get total (absolute) amount of change in the ChangeLog
    def amount(self):
        return abs(sum(self.increments))
        
    # get rate of change per 1000 years in the ChangeLog
    def rate(self):
        return round(self.amount()/(self.duration/1000),5)
    
    # get symmetry of change in the ChangeLog
    def symmetry(self):
        pos_sum = abs(sum(self.increments))
        neg_sum = abs(sum(self.opposite))
        total_sum = pos_sum + neg_sum
        score = abs(pos_sum - neg_sum)
        score = score / total_sum
        score = round(score, 3)
        return score
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # get correlations
    
    
    def correlations(self):
        for c in changes:
            if l in lineage:
                print()


def get_log(lang, feat):
    
    # get info from values
    subset = get_values(lang=lang, feat=feat)
    
    # add parent value
    parent = get_parent(lang)
    if not pd.isna(parent):
        parent_data = get_values(lang=parent, feat=feat)
        parent_data = parent_data.sort_values(by='Date').tail(1)
        if not parent_data.empty:
            subset = pd.concat([parent_data, subset], ignore_index=True)
    
    # add increment information
    subset = subset.sort_values(by='Value')
    subset['Increment'] = subset['Value'].diff().fillna(0)
    subset = subset[subset['Increment'] != 0]
    
    # return info
    return subset
    
def get_full_log(feat):
    
    # iterate over languages
    rep = pd.DataFrame()
    for l in languages.index:
        
        # get individual languages
        df = get_log(l, feat)
        rep = pd.concat([rep, df], ignore_index=True)
        
    # return the data
    return rep
    

    
### 2 ### Define the ChangeLog class
class ChangeLog:

    # initialise    
    def __init__(self, feat, lang=np.nan):
        if pd.isna(lang):
            self.df = get_full_log(feat)
            self.range = get_full_duration()
        else:
            self.df = get_log(lang, feat)
            self.range = get_duration(lang)
        self.increments = list(self.df['Increment'])
        
    # show log
    def show_log(self):
        return self.df
    
    # filter by a specific directionality of change
    def directionality(self, direction):
        self.df = self.df[self.df['Increment']*direction > 0]
        
    # get symmetry of change in this log
    def symmetry(self):
        positive_sum = sum([i for i in self.increments if i > 0])
        negative_sum = sum([i for i in self.increments if i < 0])
        total_sum = sum([abs(i) for i in self.increments])
        score = abs(positive_sum - abs(negative_sum))
        score = score / total_sum
        score = round(score, 2)
        return score
        
    # get frequency of change
    def rate(self):
        return round(sum([abs(i) for i in self.increments])/(self.range/1000),5)
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        