# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 12:39:57 2018
@author: dimit_000, Kade
"""

import os
import pandas as pd
import json

from settings import whitelist, raw_data_location, year, comments_cap, comments_csv, comment_authors_csv

comments_file = raw_data_location + 'Comments_' + year + '.txt'

comments = []
comment_count = 0
skip_count = 0
author_count = 0

# cap comments per subreddit
subreddit_comment_counts = {}
for sub in whitelist:
    subreddit_comment_counts[sub] = 0

print 'processing comments file'
for line in open(comments_file, 'r'):
    comment = json.loads(line)

    if skip_count % 100000 == 0:
        print 'skipped:' + str(skip_count)

    if comment['subreddit'] not in whitelist: # skip non political subreddits
        skip_count += 1
        continue

    if subreddit_comment_counts[comment['subreddit']] > comments_cap:
        skip_count += 1
        continue

    subreddit_comment_counts[comment['subreddit']] += 1

    comment_count += 1
    if comment_count % 1000 == 0:
        print 'added:' + str(comment_count)

    comments.append(comment)

print 'pruned ' + str(skip_count) + ' comments'
print 'used ' + str(comment_count) + ' comments'

print 'making dataframe'
comments_df = pd.DataFrame.from_dict(comments, orient='columns')

########################################## Create a users data frame from the comments
print 'Getting author data'
# make a list of authors who made comments
authors_set = set()
for row in comments_df.itertuples():
    authors_set.add(row.author)

authors_metadata_set = set()
# add users' karma used for troll detection
authors = []
for line in open(raw_data_location+'Authors_all.txt', 'r'):
    author = json.loads(line)
    author_count += 1
    if author_count % 1000000 == 0:
        print 'scanning authors:' + str(author_count)
    if author['name'] in authors_set:
        authors.append(author)

authors_df = pd.DataFrame.from_dict(authors, orient='columns')

# drop authors we don't have info on
comments_df = comments_df[comments_df.author.isin(authors_df.name)]

print 'Saving comments to csv'
comments_df.to_csv(comments_csv, sep='\t', encoding = 'utf-8')

print 'Saving authors to csv'
authors_df.to_csv(comment_authors_csv, encoding = 'utf-8')
