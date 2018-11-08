"""
Module for sharing data.
I build standard python classes/lists and panda dataframes that can be imported

@author: kade
"""

import pandas as pd

comments_file = 'data/2017_comments.csv'

class Comment:
    # attribs = ['Index', 'author', 'author_cakeday', 'author_flair_css_class', 'body', 'can_gild',
    # 'controversiality', 'created_utc', 'distinguished', 'edited', 'gilded', 'id', 'is_submitter',
    # 'link_id', 'parent_id', 'permalink', 'retrieved_on', 'score', 'stickied', 'subreddit', 'subreddit_id']

    # the 2017 data had different attributes
    attribs = ['Index', 'author', 'author_cakeday', 'author_flair_css_class', 'body', 'can_gild',
    'controversiality', 'created_utc', 'distinguished', 'edited', 'gilded', 'id',
    'link_id', 'parent_id', 'retrieved_on', 'score', 'stickied', 'subreddit', 'subreddit_id']

    def __init__(self, row):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(row, attrib))

    def __str__(self):
        return 'Author: ' + self.author + ', id: ' + str(self.id)

comments = []
comments_df = pd.read_csv(comments_file, sep='\t', encoding='utf-8')
for row in comments_df.itertuples():
    comment = Comment(row)
    comments.append(comment)
