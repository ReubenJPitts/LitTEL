# -*- coding: utf-8 -*-

"""
LitTEL

@name:     timelineage.py
@date:     26/06/2023
@author:   Reuben J. Pitts

This script defines a TimeLineage

A TimeLineage object provides information about the LitTEl data for a specific LANGUAGE (expressed as a Glottocode)

"""


### 0 ### Imports

# littel imports
from littel.processing import values
from littel.functions import dict_merge, get_duration, get_lineage

# library imports
import pandas as pd
import numpy as np

# filter values
changes = values[values['Increment'] != 0]
changes = changes[['Feature_ID','Language_ID','Date','Increment','Direction']]


### 1 ### Define the TimeLineage class

class TimeLineage:
    
    # initialise the TimeLineage
    def __init__(self, lang):
        self.current = changes[changes['Language_ID'] == lang]
        
        lineage = get_lineage(lang)
        lineage.remove(lang)
        self.lineage = lineage
        
        self.past = self.current.copy()
        for l in lineage:
            subset = changes[changes['Language_ID'] == l]
            self.past = pd.concat([self.past, subset], ignore_index=True)
        self.past = self.past.sort_values(by='Date')
        
        self.range = get_duration(lang)
    
    # get increments for a feature and a directionality
    def increments(self, feat, drct=np.nan):
        increment = self.current[self.current['Feature_ID'] == feat]
        increment = list(increment['Increment'])
        if not pd.isna(drct):
            if drct == 1:
                increment = [i for i in increment if i > 0]
            if drct == 0:
                increment = [i for i in increment if i < 0]
        return increment

    # get changes preceding a particular date
    def correlations(self, date):
        corr = self.past[self.past['Date'] <= date].copy()
        corr['Distance'] = [abs(date - i) for i in corr['Date']]
        corr = corr.set_index(['Feature_ID','Direction'])['Distance'].to_dict()
        return corr
    
    # get dates relating to a feature and directionality
    def change(self, feat, drct):
        change = self.current.copy()
        change = change[change['Feature_ID'] == feat]
        change = change[change['Direction'] == drct]
        return list(change['Date'])
    
    # get correlations for a feature and directionality
    def change_correlations(self, feat, drct):
        change = self.change(feat, drct)
        corrs = [self.correlations(c) for c in change]
        corrs = dict_merge(corrs)
        return corrs
            
        
        

