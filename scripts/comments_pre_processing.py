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
from subreddits import subreddits
from settings import whitelist

comment_json_attributes_to_save = ['author', 'body', 'controversiality',
'gilded', 'id', 'score', 'subreddit', 'subreddit_id']

comments_file = '/Volumes/TIME/reddit data/RC_2016_filtered.txt'

invalid_names = set(['[deleted]', 'ithinkisaidtoomuch', 'Concise_AMA_Bot', 'AutoModerator'])
valid_subs = set(map(lambda x: x.name, subreddits))

comments = []
comment_count = 0
skip_count = 1
subreddit_comment_counts = {}
for sub in whitelist:
    subreddit_comment_counts[sub] = 0

print 'about to read the file'
for line in open(comments_file, 'r'):
    comment = json.loads(line)

    # sanitize the comment body
    comment['body'] = re.sub('[^A-Za-z0-9]+', ' ', comment['body'])

    if skip_count % 100000 == 0:
        print 'skipped:' + str(skip_count)

    if comment['subreddit'] not in whitelist: # skip non political subreddits
        skip_count += 1
        continue

    if comment['author'] in invalid_names: # skip problem comments
        skip_count += 1
        continue

    # if comment['subreddit'] not in valid_subs: # skip long tail of niche subreddits
    #     # print comment['subreddit']
    #     skip_count += 1
    #     continue

    # if comment['subreddit'] in blacklist: # skip popular non political subreddits
    #     skip_count += 1
    #     continue

    if subreddit_comment_counts[comment['subreddit']] > 1000:
        skip_count += 1
        continue

    subreddit_comment_counts[comment['subreddit']] += 1

    comment_count += 1
    if comment_count % 1000 == 0:
        print 'added:' + str(comment_count)

    # don't save unnecessary stuff
    new_comment = {}
    for attrib in comment_json_attributes_to_save:
        new_comment[attrib] = comment[attrib]

    comments.append(new_comment)

print 'pruned ' + str(skip_count) + ' comments'
print 'used ' + str(comment_count) + ' comments'

print subreddit_comment_counts

print 'making dataframe'
comments_df = pd.DataFrame.from_dict(comments, orient='columns')

print 'Saving comments to csv'
comments_df.to_csv('data/2016_comments_whitelist_capped.csv', sep='\t', encoding = 'utf-8')

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

users_df.to_csv('data/2016_users_whitelist_capped.csv', encoding = 'utf-8')

# Authors: includes users' karma used for troll detection
users_df = pd.read_csv('data/2017_users_whitelist_capped.csv', encoding = 'utf-8')
authors = []
for line in open('data/all_authors.json', 'r'):
    author = json.loads(line)
    if author['name'] in users_df.name.values:
        authors.append(author)

authors_df = pd.DataFrame.from_dict(authors, orient='columns')
authors_df.to_csv('data/2017_authors.csv', encoding = 'utf-8')
