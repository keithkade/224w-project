import pandas as pd

subreddits_file = 'data/subreddits_basic.csv'

class SubReddit:
    # attribs = ['Index', 'base10_id', 'base36_id', 'creation_epoch', 'name', 'subscriber_count']
    attribs = ['Index', 'base36_id', 'name']

    def __init__(self, row):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(row, attrib))

    def __str__(self):
        return 'Subreddit name: ' + self.name + ', id: ' + str(self.base36_id)

subreddits = []
subreddits_df = pd.read_csv(subreddits_file, encoding='utf-8')
for row in subreddits_df.itertuples():
    subreddit = SubReddit(row)
    subreddits.append(subreddit)
