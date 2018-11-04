import pandas as pd

users_file = 'data/sample_users.csv'

class User:
    attribs = ['Index', 'name']

    def __init__(self, row):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(row, attrib))

    def __str__(self):
        return 'Name: ' + self.name

users = []
users_df = pd.read_csv(users_file, encoding='utf-8')
for row in users_df.itertuples():
    user = User(row)
    users.append(user)
