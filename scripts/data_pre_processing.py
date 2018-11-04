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

comments_df.to_csv('data/sample_comments.csv', sep='\t', encoding = 'utf-8')

########################################## Create a users data frame from the comments
authors_set = set()
for row in comments_df.itertuples():
    authors_set.add(row.author)

# make a list
users_jsons = []
for author in authors_set:
    users_jsons.append({'name': author})

# then a dataframe
users_df = pd.DataFrame(users_jsons)

users_df.to_csv('data/sample_users.csv', encoding = 'utf-8')
