# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 12:39:57 2018
@author: dimit_000, Kade
"""

import pandas as pd
import json
from settings import whitelist, raw_data_location, year, posts_cap, posts_csv, post_authors_csv

posts_file = raw_data_location + 'Posts_' + year + '.txt'

posts = []
post_count = 0
skip_count = 0
author_count = 0

subreddit_post_counts = {}
for sub in whitelist:
    subreddit_post_counts[sub] = 0

print 'processing posts file'

for line in open(posts_file, 'r'):
    post = json.loads(line)

    if skip_count % 1000000 == 0:
        print 'skipped:' + str(skip_count)

    if subreddit_post_counts[post['subreddit']] > posts_cap:
        skip_count += 1
        continue

    subreddit_post_counts[post['subreddit']] += 1

    post_count += 1
    if post_count % 1000 == 0:
        print 'added:' + str(post_count)

    posts.append(post)

print 'pruned ' + str(skip_count) + ' posts'
print 'used ' + str(post_count) + ' posts'

print 'making dataframe'
posts_df = pd.DataFrame.from_dict(posts, orient='columns')



########################################## Create a users data frame from the posts
print 'Getting author data'
# make a list of authors who made posts
authors_set = set()
for row in posts_df.itertuples():
    authors_set.add(row.author)

# add users' karma used for troll detection
authors = []
for line in open(raw_data_location+'Authors_all.txt', 'r'):
    author = json.loads(line)
    author_count += 1
    if author_count % 100000 == 0:
        print 'scanning authors:' + str(author_count)
    if author['name'] in authors_set:
        authors.append(author)


authors_df = pd.DataFrame.from_dict(authors, orient='columns')

# drop authors we don't have info on
posts_df = posts_df[posts_df.author.isin(authors_df.name)]

print 'Saving posts to csv'
posts_df.to_csv(posts_csv, sep='\t', encoding = 'utf-8')

print 'Saving authors to csv'
authors_df.to_csv(post_authors_csv, encoding = 'utf-8')
