"""
Module for sharing data.
I build standard python classes/lists and panda dataframes that can be imported

@author: kade
"""

import pandas as pd
from settings import posts_csv

class Post:
    attribs = ['author', 'subreddit', 'subreddit_id',
    'selftext', 'score', 'score', 'num_comments', 'id', 'title', 'ups', 'downs', 'Index']

    def __init__(self, row):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(row, attrib))

    def __str__(self):
        return 'Post subreddit: ' + self.name + ', id: ' + str(self.id) + ' Index: ' + str(self.Index)

posts = []
posts_df = pd.read_csv(posts_csv, sep='\t', encoding='utf-8')
for row in posts_df.itertuples():
    post = Post(row)
    posts.append(post)
