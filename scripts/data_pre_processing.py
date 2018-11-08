# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 12:39:57 2018

@author: dimit_000
"""

import os
import pandas as pd
import json
import re
from pprint import pprint

comments_file = '/Volumes/TIME/reddit data/RC_2017-05.txt'

invalid_names = set(['[deleted]', 'ithinkisaidtoomuch', 'Concise_AMA_Bot'])

comments = []
comment_count = 0
for line in open(comments_file, 'r'):
    comment = json.loads(line)

    # sanitize the comment body
    comment['body'] = re.sub('[^A-Za-z0-9]+', ' ', comment['body'])

    if comment['author'] in invalid_names: # skip problem comments
        continue

    comment_count += 1
    print comment_count

    if comment_count > 20000:
        break
    comments.append(comment)

comments_df = pd.DataFrame([])
for comment in comments:
    df = pd.DataFrame.from_dict([comment], orient='columns')
    comments_df = comments_df.append(df)

print 'Saving comments to csv'
comments_df.to_csv('data/2017_comments_sanitized.csv', sep='\t', encoding = 'utf-8')

########################################## Create a users data frame from the comments
print 'Calculating authors'
authors_set = set()
for row in comments_df.itertuples():
    authors_set.add(row.author)

# make a list
users_jsons = []
for author in authors_set:
    users_jsons.append({'name': author})

# then a dataframe
users_df = pd.DataFrame(users_jsons)

print 'Saving comments to csv'
users_df.to_csv('data/2017_users_sanitized.csv', encoding = 'utf-8')
