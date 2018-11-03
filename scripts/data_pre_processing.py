# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 12:39:57 2018

@author: dimit_000
"""

import os
import pandas as pd
import json
from pprint import pprint

comments_file = 'data/sample_comments.json'
    
comments = []
for line in open(comments_file, 'r'):
    comments.append(json.loads(line))

comments_df = pd.DataFrame([])
for comment in comments:
    df = pd.DataFrame.from_dict([comment], orient='columns')
    comments_df = comments_df.append(df)
    
