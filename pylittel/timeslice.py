# -*- coding: utf-8 -*-

"""
LitTEL

@name:     timeslice.py
@date:     26/06/2023
@author:   Reuben J. Pitts

This script defines a TimeSlice

A TimeSlice object provides information by a FEATURE and a DATE
- A feature is expressed as a Feature_ID (e.g. 'Pos_Coord')
- A date is expressed as a positive or negative integer (e.g. -200)


"""


### 0 ###

# define the function for getting slice information
def get_slice(date, feat):
    
    # get a subset of the data
    subset = get_values(feat=feat)
    
    # group by languages
    groups = subset.groupby('Language_ID')
    
    # iterate over the groups
    sl = []
    for lang, df in groups:
    
        # check if the date is in range
        date_range = get_timespan(lang)
        if date_range[0] < date <= date_range[1]:
            
            # turn data into dictionary
            dt = df.set_index('Date')['Value'].to_dict()

            # check if exact date happens to be present
            value = dt.get(date,np.nan)
        
            # get preceding and following value
            value_before = dt.get(max((i for i in dt.keys() if i < date), default=None), np.nan)
            value_after = dt.get(min((i for i in dt.keys() if i > date), default=None), np.nan)
                
            # get parent value
            if pd.isna(value_before):
                parent = get_parent(lang)
                value_before = get_last_value(parent, feat)
                        
            # take average of before and after
            if pd.isna(value):
                value = np.mean((value_before, value_after))
        
            # if value_before and value_parent are both != NaN, take their mean
            if pd.isna(value):
                value = value_before if pd.isna(value_after) else value_after

            # add to the repository
            if not pd.isna(value):
                sl.append([lang, value])
        
    # make repository into dataframe
    sl = pd.DataFrame(data=sl, columns=["Language_ID","Value"])
        
    # return repository
    return sl
            

# define the TimeSlice class
class TimeSlice:
    
    # initialise
    def __init__(self, date, feat):
        self.df = get_slice(date, feat)
        self.languages = list(self.df['Language_ID'])
        self.values = list(self.df['Value'])
        self.date = date
        self.dictionary = self.df.set_index('Language_ID')['Value'].to_dict()
    
    # return a list for matrix
    def matrix_column(self):
        rep = []
        for l in sorted(languages.index):
            rep.append(self.dictionary.get(l,np.nan))
    
    # get latitudes
    def latitude(self, subset=np.nan):
        rep = []
        for l,v in zip(self.languages,self.values):
            if pd.isna(subset) or v == subset:
                rep.append(get_latitude(l))
        return rep
            
    # get longitudes
    def longitude(self, subset=np.nan):
        rep = []
        for l,v in zip(self.languages,self.values):
            if pd.isna(subset) or v == subset:
                rep.append(get_longitude(l)) 
        return rep

    # get names
    def names(self, subset=np.nan):
        rep = []
        for l,v in zip(self.languages,self.values):
            if pd.isna(subset) or v == subset:
                name = str(get_name(l))
                if get_attestation_status(l, self.date) == False:
                    name = "*" + name
                rep.append(name)
        return rep

    # return text labels for a map
    def labels(self):
        return zip(self.longitude(), self.latitude(), self.names())

        
        
