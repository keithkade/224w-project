# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 12:39:57 2018
@author: dimit_000
"""

import pandas as pd
import json
from settings import whitelist

posts_file = '/Volumes/TIME/reddit data/RS_2016_filtered.txt'

posts = []
post_count = 0
skip_count = 1
subreddit_post_counts = {}
for sub in whitelist:
    subreddit_post_counts[sub] = 0

print 'about to read the file'
for line in open(posts_file, 'r'):
    post = json.loads(line)

    if skip_count % 100000 == 0:
        print 'skipped:' + str(skip_count)

    if subreddit_post_counts[post['subreddit']] > 1000:
        skip_count += 1
        continue

    subreddit_post_counts[post['subreddit']] += 1

    post_count += 1
    if post_count % 1000 == 0:
        print 'added:' + str(post_count)

    posts.append(post)

print 'pruned ' + str(skip_count) + ' posts'
print 'used ' + str(post_count) + ' posts'

print subreddit_post_counts

print 'making dataframe'
posts_df = pd.DataFrame.from_dict(posts, orient='columns')

print 'Saving comments to csv'
posts_df.to_csv('data/2016_posts_whitelist_capped.csv', sep='\t', encoding = 'utf-8')

########################################## Create a users data frame from the comments
print 'Calculating authors'
authors_set = set()
for row in posts_df.itertuples():
    authors_set.add(row.author)

# make a list
users_jsons = []
for author in authors_set:
    users_jsons.append({'name': author})

# then a dataframe
users_df = pd.DataFrame(users_jsons)
users_df.to_csv('data/2016_post_authors.csv', encoding = 'utf-8')
