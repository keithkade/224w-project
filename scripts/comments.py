"""
Module for sharing data.
I build standard python classes/lists and panda dataframes that can be imported

@author: kade
"""

import pandas as pd
from settings import comments_csv

class Comment:
    # attribs = ['Index', 'author', 'author_cakeday', 'author_flair_css_class', 'body', 'can_gild',
    # 'controversiality', 'created_utc', 'distinguished', 'edited', 'gilded', 'id', 'is_submitter',
    # 'link_id', 'parent_id', 'permalink', 'retrieved_on', 'score', 'stickied', 'subreddit', 'subreddit_id']

    # the 2017 data had different attributes
    # attribs = ['Index', 'author', 'author_cakeday', 'author_flair_css_class', 'body', 'can_gild',
    # 'controversiality', 'created_utc', 'distinguished', 'edited', 'gilded', 'id',
    # 'link_id', 'parent_id', 'retrieved_on', 'score', 'stickied', 'subreddit', 'subreddit_id']

    # stuff worth saving
    attribs = ['Index', 'author', 'body', 'controversiality',
    'gilded', 'id', 'score', 'subreddit', 'subreddit_id']

    def __init__(self, row):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(row, attrib))

    def __str__(self):
        return 'Author: ' + self.author + ', id: ' + str(self.id)

comments = []
comments_df = pd.read_csv(comments_csv, sep='\t', encoding='utf-8')
for row in comments_df.itertuples():
    comment = Comment(row)
    comments.append(comment)

def count_sub_comments():
    subreddit_counts = {}
    for comment in comments:
        if comment.subreddit in subreddit_counts:
            subreddit_counts[comment.subreddit] += 1
        else:
            subreddit_counts[comment.subreddit] = 1

    subs_sorted = []
    for sub in subreddit_counts:
        subs_sorted.append((subreddit_counts[sub], sub))

    print 'Total comments: ' + str(len(comments))
    # Making a 'blacklist' of super popular subs we don't care about. ex: AskReddit
    print sorted(subs_sorted, reverse=True)[0:20]
    # print map(lambda x: x[1], sorted(subs_sorted, reverse=True)[0:40])

def count_author_comments():
    author_counts = {}
    for comment in comments:
        if comment.author in author_counts:
            author_counts[comment.author] += 1
        else:
            author_counts[comment.author] = 1

    authors_sorted = []
    for sub in author_counts:
        authors_sorted.append((author_counts[sub], sub))

    print sorted(authors_sorted, reverse=True)[0:20]
    # print map(lambda x: x[1], sorted(subs_sorted, reverse=True)[0:40])

count_sub_comments()
count_author_comments()
