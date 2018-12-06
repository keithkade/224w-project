"""
Module for sharing data.
I build standard python classes/lists and panda dataframes that can be imported

@author: kade
"""

import pandas as pd
from settings import subreddits_csv

class SubReddit:
    # attribs = ['Index', 'base10_id', 'base36_id', 'creation_epoch', 'name', 'subscriber_count']
    attribs = ['Index', 'base36_id', 'name', 'subscriber_count']

    def __init__(self, row):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(row, attrib))

    def __str__(self):
        return 'Subreddit name: ' + self.name + ', id: ' + str(self.base36_id) + ' Index: ' + str(self.Index)

subreddits = []
subreddits_df = pd.read_csv(subreddits_csv, encoding='utf-8')
for row in subreddits_df.itertuples():
    subreddit = SubReddit(row)
    subreddits.append(subreddit)
