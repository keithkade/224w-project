import os
import pandas as pd
import json
import re
from settings import whitelist

posts_files = ['/Volumes/TIME/reddit data/RS_2016-01', '/Volumes/TIME/reddit data/RS_2016-02', '/Volumes/TIME/reddit data/RS_2016-03']
out_file = '/Volumes/TIME/reddit data/RS_2016_filtered.txt'

invalid_names = set(['[deleted]'])

post_json_attributes_to_save = ['author', 'subreddit', 'subreddit_id',
'selftext', 'score', 'score', 'num_comments', 'id', 'title', 'ups', 'downs']

skip_count = 0
post_count = 0
with open(out_file, 'a') as f:
    for posts_file in posts_files:
        for line in open(posts_file, 'r'):
            post = json.loads(line)

            # sanitize the comment body
            post['selftext'] = re.sub('[^A-Za-z0-9]+', ' ', post['selftext'])
            post['title'] = re.sub('[^A-Za-z0-9]+', ' ', post['title'])

            if skip_count % 100000 == 0:
                print 'skipped:' + str(skip_count)

            if 'subreddit' not in post or post['subreddit'] not in whitelist: # skip non political subreddits
                skip_count += 1
                continue

            if post['author'] in invalid_names: # skip problem comments
                skip_count += 1
                continue

            post_count += 1

            if post_count % 10000 == 0:
                print 'added:' + str(post_count)

            # don't save unnecessary stuff
            new_post = {}
            for attrib in post_json_attributes_to_save:
                new_post[attrib] = post[attrib]

            # write the comment to a new file
            f.write(json.dumps(new_post) + os.linesep)
