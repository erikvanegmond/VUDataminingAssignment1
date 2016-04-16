# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 14:29:36 2016

@author: Celeste
"""

import pandas as pd

filepath = 'data/dataset_mood_smartphone.csv'

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
df = pd.read_csv(filepath, parse_dates=['time'], index_col='time', date_parser=dateparse)
print "data opened"


data = df.loc[(df['variable'] == 'mood')]
        
print         
a = pd.DataFrame(data, index = df.index)
print a