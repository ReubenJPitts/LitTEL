# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 21:06:08 2023

@author: u0107389
"""

### 0 ### Imports

# libraries
import pandas as pd
import numpy as np

# import LitTEL
from littel.processing import languages
from littel.processing import codes
from littel.processing import values
from littel.processing import features

# create some dictionaries from languages to speed up the code
language_parents = languages['Parent'].to_dict()
language_lats = languages['Latitude'].to_dict()
language_lons = languages['Longitude'].to_dict()
language_early = languages['Earliest'].to_dict()
language_late = languages['Latest'].to_dict()
language_parent_date = languages['Parent_Date'].to_dict()
language_names = languages['Name'].to_dict()


### 1 ### Convenience functions for human-readable descriptions

def get_id(name):
    subset = languages[languages['Name'] == name]
    if len(subset) == 0:
        subset = languages[languages['Name'].str.contains(name)]
    return list(subset.index)

def get_name(glottocode):
    if pd.isna(glottocode):
        return np.nan
    return language_names.get(glottocode, np.nan)
 
def get_code(feat, value):
    subset = codes.copy()
    subset = subset[subset['Feature_ID'] == feat]
    subset = subset[subset['Value'] == value]
    if subset.empty:
        return ''
    return list(subset['Description'])[0]

def get_feature(feat):
    subset = features.copy()
    subset = subset[subset['Feature_ID'] == feat]
    if subset.empty:
        return ''
    return list(subset['Description'])[0]

def get_date(date):
    if date > 0:
        readable_date = str(date) + ' CE'
    elif date <= 0:
        readable_date = str(abs(date-1)) + ' BCE'
    return readable_date


### 2 ### Dealing with parents and lineages

def get_parent(lang):
    if pd.isna(lang):
        return np.nan
    return language_parents.get(lang, np.nan)

def get_lineage(p):
    rep = []
    while not pd.isna(p):
        rep.append(p)
        p = get_parent(p)
    return rep


### 3 ### Attestation ranges

def get_early(lang):
    if pd.isna(lang):
        return np.nan
    return language_early.get(lang, np.nan)

def get_late(lang):
    if pd.isna(lang):
        return np.nan
    return language_late.get(lang, np.nan)

def get_parent_date(lang):
    if pd.isna(lang):
        return np.nan
    return language_parent_date.get(lang, np.nan)
    
def get_timespan(lang):
    parent_date = get_parent_date(lang)
    late = get_late(lang)
    if not pd.isna(parent_date):
        early = parent_date
    else:
        early = get_early(lang)
    return (early, late)

def get_duration(lang):
    a,b = get_timespan(lang)
    return abs(a-b)

def get_attestation_status(lang, date):
    if pd.isna(lang) or pd.isna(date):
        return np.nan
    if get_early(lang) <= date <= get_late(lang):
        return True
    else:
        return False


### 4 ### Geography

def get_latitude(lang):
    if pd.isna(lang):
        return np.nan
    return language_lats.get(lang, np.nan)
    
def get_longitude(lang):
    if pd.isna(lang):
        return np.nan
    return language_lons.get(lang, np.nan)


### 5 ### Getting data

def get_values(lang=np.nan, feat=np.nan, date=np.nan):
    subset = values.copy()
    subset = subset[subset['Value'].notna()]
    if not pd.isna(lang):
        subset = subset[subset['Language_ID'] == lang]
    if not pd.isna(feat):
        subset = subset[subset['Feature_ID'] == feat]
    if not pd.isna(date):
        subset = subset[subset['Date'] == date]
    return subset

def get_last_value(lang, feat, n=-1):
    if pd.isna(lang) or pd.isna(feat) or pd.isna(n):
        return np.nan
    subset = get_values(lang=lang, feat=feat)
    subset = subset.sort_values(by='Date')
    subset = list(subset['Value'])
    if len(subset) > 0:
        return subset[n]
    else:
        return np.nan
    
    
### 6 ### Merge dictionaries

def dict_merge(dicts):
    mdict = {}
    for d in dicts:
        for key, value in d.items():
            if key in mdict:
                mdict[key] = min(mdict[key], value)
            else:
                mdict[key] = value
    return mdict
