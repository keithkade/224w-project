"""
Module for sharing data.
I build standard python classes/lists and panda dataframes that can be imported

@author: kade
"""

import pandas as pd
from settings import comment_authors_csv, post_authors_csv

class User:
    attribs = ['Index', 'name']

    def __init__(self, row):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(row, attrib))

    def __str__(self):
        return 'Name: ' + self.name


# combine post and comment authors
comment_authors_df = pd.read_csv(comment_authors_csv, encoding='utf-8')
post_authors_df = pd.read_csv(post_authors_csv, encoding='utf-8')
users_df = comment_authors_df.append(post_authors_df, ignore_index=True)

# drop dups
users_df = users_df[~users_df.index.duplicated(keep='first')]

users = []
for row in users_df.itertuples():
    user = User(row)
    users.append(user)
