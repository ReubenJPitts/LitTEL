# -*- coding: utf-8 -*-

"""
LitTEL

@name:     processing.py
@date:     26/06/2023
@author:   Reuben J. Pitts

This script imports the four csv files, cleans them up and enriches them.

"""


### 0 ### Imports

# libraries
import pandas as pd
import numpy as np

# files
values = pd.read_csv('values.csv', sep=',')
languages = pd.read_csv('languages.csv', sep=',')
features = pd.read_csv('features.csv', sep=',')
codes = pd.read_csv('codes.csv', sep=',')


### 1 ### modifications to languages.csv

# clean up a bit
languages['ID'] = [i.strip() for i in languages['ID']]
languages = languages.drop_duplicates(subset='ID')
languages = languages.sort_values(by=['Name'])
languages = languages.set_index('ID')

# set default starting date
languages['Earliest'] = languages['Earliest'].fillna(languages['Floruit'])
languages['Earliest'] = languages['Earliest'].fillna(-1000)

# set default end date
languages['Latest'] = languages['Latest'].fillna(languages['Floruit'])
languages['Latest'] = languages['Latest'].fillna(1000)

# add an average 'floruit', if missing
languages['Floruit'] = languages['Floruit'].fillna(languages[['Earliest', 'Latest']].mean(axis=1))

# add last parent date, if relevant
languages['Parent_Date'] = languages['Parent'].map(languages['Latest'])


### 2 ### modifications to values.csv

# clean up a bit
values['Language_ID'] = [i.strip() for i in values['Language_ID']]
values = values.sort_values(by=['Language_ID', 'Feature_ID', 'Date'])
values = values.reset_index(drop=True)

# add a date
values['Floruit'] = [languages.loc[i]['Floruit'] for i in list(values['Language_ID'])]
values['Date'] = values['Date'].fillna(values['Floruit'])

# remove NaN values
values = values.dropna(subset='Value')


### 3 ### add an increment column to values.csv

# get a dictionary of final values by language and feature
lasts = values.groupby(['Language_ID','Feature_ID'])['Date'].idxmax()
lasts = values[values.index.isin(lasts)]
lasts = lasts.set_index(['Language_ID','Feature_ID'])['Value'].to_dict()

# get a dictionary of parent glottocodes
language_parents = languages['Parent'].to_dict()

# get parent increment
def get_parent_increment(row):
    parent = language_parents.get(row['Language_ID'],np.nan)
    feature = row['Feature_ID']
    parent_value = lasts.get((parent, feature),np.nan)
    value = row['Value']
    return parent_value - value

# add an increment column
values['Increment'] = values.groupby(['Language_ID','Feature_ID'])['Value'].diff()

# try filling NaNs with parent increments
values['Increment'] = values['Increment'].fillna(values.apply(lambda row: get_parent_increment(row), axis=1))

# if not, fill NaNs with 0
values['Increment'] = values['Increment'].fillna(0)

# add a direction column
values['Direction'] = [1 if i > 0 else 0 for i in values['Increment']]



