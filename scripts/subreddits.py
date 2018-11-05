"""
Module for sharing data.
I build standard python classes/lists and panda dataframes that can be imported

@author: kade
"""

import pandas as pd

subreddits_file = 'data/subreddits_basic.csv'

class SubReddit:
    # attribs = ['Index', 'base10_id', 'base36_id', 'creation_epoch', 'name', 'subscriber_count']
    attribs = ['Index', 'base36_id', 'name', 'subscriber_count']

    def __init__(self, row):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(row, attrib))

    def __str__(self):
        return 'Subreddit name: ' + self.name + ', id: ' + str(self.base36_id) + ' Index: ' + str(self.Index)

subreddits = []
subreddits_df = pd.read_csv(subreddits_file, encoding='utf-8')
for row in subreddits_df.itertuples():
    subreddit = SubReddit(row)
    subreddits.append(subreddit)

def get_filtered_subreddits(n):
    popular_subs = []
    newIndex = 0
    for sub in subreddits:
        if sub.subscriber_count != 'None' and int(sub.subscriber_count) > n:
            sub.Index = newIndex
            newIndex += 1
            popular_subs.append(sub)

    return popular_subs
