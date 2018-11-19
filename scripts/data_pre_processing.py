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
from settings import subreddit_subscriber_cutoff
from subreddits import get_filtered_subreddits

subreddits = get_filtered_subreddits(subreddit_subscriber_cutoff)

comment_json_attributes_to_save = ['author', 'body', 'controversiality',
'gilded', 'id', 'score', 'subreddit', 'subreddit_id']

comments_file = '/Volumes/TIME/reddit data/RC_2017-05.txt'

invalid_names = set(['[deleted]', 'ithinkisaidtoomuch', 'Concise_AMA_Bot', 'AutoModerator'])
valid_subs = set(map(lambda x: x.name, subreddits))
# mostly the defaults. also some with weirdly high comment count, and non-political ones
blacklist = set(['AskReddit', 'funny', 'pics', 'gaming', 'videos', 'movies',
'mildlyinteresting', 'OldSchoolCool', 'todayilearned', 'AdviceAnimals', 'gifs',
'aww', 'blog', 'books', 'food', 'askscience', 'Showerthoughts', 'photoshopbattles',
'photoshopbattles', 'gonewild', 'forhonor', 'RocketLeagueExchange', 'RocketLeague',
'Sneakers', 'GamingCircleJerk', 'counting', 'darksouls3', 'Warhammer40k',
'EliteDangerous', 'DnD', 'hearthstone', 'Drugs', 'Bitcoin', 'Anime', 'Ice_Poseidon'])

comments = []
comment_count = 0
skip_count = 0

print 'about to read the file'
for line in open(comments_file, 'r'):
    comment = json.loads(line)

    # sanitize the comment body
    comment['body'] = re.sub('[^A-Za-z0-9]+', ' ', comment['body'])

    if comment['author'] in invalid_names: # skip problem comments
        skip_count += 1
        continue

    if comment['subreddit'] not in valid_subs: # skip long tail of niche subreddits
        # print comment['subreddit']
        skip_count += 1
        continue

    if comment['subreddit'] in blacklist: # skip popular non political subreddits
        skip_count += 1
        continue

    comment_count += 1
    print comment_count

    if comment_count > 1000000:
        break

    # don't save unnecessary stuff
    new_comment = {}
    for attrib in comment_json_attributes_to_save:
        new_comment[attrib] = comment[attrib]

    comments.append(new_comment)

print 'pruned ' + str(skip_count) + ' comments'

print 'making dataframe'
comments_df = pd.DataFrame.from_dict(comments, orient='columns')

print 'Saving comments to csv'
comments_df.to_csv('data/2017_comments_1m_trimmed.csv', sep='\t', encoding = 'utf-8')

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
<<<<<<< HEAD
users_df.to_csv('data/2017_users_trimmed.csv', encoding = 'utf-8')


# Authors: includes users' karma used for troll detection
authors = []
for line in open('data\2016_authors.json', 'r'):
    author = json.loads(line)
    if author['name'] in users_df.name.values:
        authors.append(author)
=======
users_df.to_csv('data/2017_users_1m_trimmed.csv', encoding = 'utf-8')
>>>>>>> 6b7144e258b22154ae311b15047ffffc922b2322
