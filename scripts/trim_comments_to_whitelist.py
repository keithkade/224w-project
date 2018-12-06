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

# note: this file has 79,810,360 comments
comments_files = ['/Volumes/TIME/reddit data/RC_2016-01', '/Volumes/TIME/reddit data/RC_2016-02', '/Volumes/TIME/reddit data/RC_2016-03']

out_file = '/Volumes/TIME/reddit data/RC_2016_filtered.txt'

invalid_names = set(['[deleted]', 'ithinkisaidtoomuch', 'Concise_AMA_Bot', 'AutoModerator'])

comment_count = 0
skip_count = 0

# os.remove(out_file)
with open(out_file, 'a') as f:
    for comments_file in comments_files:
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

            comment_count += 1
            if comment_count % 100000 == 0:
                print 'added:' + str(comment_count)

            # don't save unnecessary stuff
            new_comment = {}
            for attrib in comment_json_attributes_to_save:
                new_comment[attrib] = comment[attrib]

            # write the comment to a new file
            f.write(json.dumps(new_comment) + os.linesep)
