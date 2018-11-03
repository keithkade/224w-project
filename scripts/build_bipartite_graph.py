"""
This file reads a subreddit list and a comment list and creates a bipartite graph based on comments.
I build standard python classes/lists and panda dataframes for Users, SubReddits, and Comments.

lists:
comments, subreddits, users

dataframes:
comments_df, subreddits_df, users_df

I also populate a couple maps, user_to_node_id and subreddit_id_to_node_id, for util purposes

@author: kade
"""

import pandas as pd
import snap

################################################ Consts

subreddits_file = 'data/subreddits_basic.csv'
comments_file = 'data/sample_comments.csv'

################################################ Globals that get used later
subreddit_id_to_node_id = {}
user_to_node_id = {}

################################################ Utility classes. Might come in handy later

class User:
    attribs = ['Index', 'name']

    def __init__(self, row):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(row, attrib))

    def __str__(self):
        return 'Name: ' + self.name

class SubReddit:
    attribs = ['Index', 'base10_id', 'base36_id', 'creation_epoch', 'name', 'subscriber_count']

    def __init__(self, row):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(row, attrib))

    def __str__(self):
        return 'Subreddit name: ' + self.name + ', id: ' + str(self.base10_id)

class Comment:
    attribs = ['Index', 'author', 'author_cakeday', 'author_flair_css_class', 'body', 'can_gild',
    'controversiality', 'created_utc', 'distinguished', 'edited', 'gilded', 'id', 'is_submitter',
    'link_id', 'parent_id', 'permalink', 'retrieved_on', 'score', 'stickied', 'subreddit', 'subreddit_id']

    def __init__(self, row):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(row, attrib))

    def __str__(self):
        return 'Author: ' + self.author + ', id: ' + str(self.id)

################################################ Utility functions

def get_node_id_by_subreddit_id(subbredit_id):
    if subbredit_id in subreddit_id_to_node_id:
        return subreddit_id_to_node_id[subbredit_id]
    # print 'ERROR: Could not find subbredit_id: ' + str(subbredit_id)
    return None

def get_node_id_by_author(name):
    if name in user_to_node_id:
        return user_to_node_id[name]
    # print 'ERROR: Could not find user: ' + name
    return None

################################################ load and format the data

####### subreddits
subreddits = []
subreddits_df = pd.read_csv(subreddits_file, encoding='utf-8')
for row in subreddits_df.itertuples():
    subreddit = SubReddit(row)
    subreddits.append(subreddit)


####### comments
authors_set = set()
comments = []
comments_df = pd.read_csv(comments_file, sep='\t', encoding='utf-8')
for row in comments_df.itertuples():
    comment = Comment(row)
    comments.append(comment)
    authors_set.add(comment.author)

####### users
# make a list
users_jsons = []
for author in authors_set:
    users_jsons.append({'name': author})

# then a dataframe
users_df = pd.DataFrame(users_jsons)

users = []
for row in users_df.itertuples():
    user = User(row)
    users.append(user)

################################################ build the graph

subreddit_count = len(subreddits)
user_count      = len(users)

bipartite_graph = snap.TUNGraph.New()

# Add the nodes

for subreddit in subreddits:
    bipartite_graph.AddNode(subreddit.Index)
    subreddit_id_to_node_id[subreddit.base36_id] = subreddit.Index

# offset by the number of subreddits
for user in users:
    bipartite_graph.AddNode(user.Index + subreddit_count)
    user_to_node_id[user.name] = user.Index + subreddit_count

# Add the edges

# this is the simplest way to say an author and a user are connected.
for comment in comments:
    subreddit_node_id = get_node_id_by_subreddit_id(comment.subreddit_id)
    user_node_id      = get_node_id_by_author(comment.author)

    if subreddit_node_id != None and user_node_id != None:
        bipartite_graph.AddEdge(subreddit_node_id, user_node_id)

# TODO alternative ways to decide if user and subreddit are connected

print 'Nodes: ' + str(bipartite_graph.GetNodes())
print 'Edges: ' + str(bipartite_graph.GetEdges())

print 'Saving binary'
FOut = snap.TFOut("graphs/bipartite_connected_by_comment.graph")
bipartite_graph.Save(FOut)
FOut.Flush()
