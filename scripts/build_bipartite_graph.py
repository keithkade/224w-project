"""
This file creates a bipartite graph based on comments.

I also populate a couple maps, user_to_node_id and subreddit_id_to_node_id, for util purposes

@author: kade
"""
import sys
sys.path.append('scripts/')

import pandas as pd
import snap
from subreddits import subreddits
from users import users
from comments import comments


################################################ Globals that get used later

subreddit_id_to_node_id = {}
user_to_node_id = {}

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

################################################ build the graph

subreddit_count = len(subreddits)
user_count      = len(users)

bipartite_graph = snap.TUNGraph.New()

# Add the nodes

for subreddit in subreddits:
    bipartite_graph.AddNode(int(subreddit.Index))
    subreddit_id_to_node_id[subreddit.base36_id] = subreddit.Index

# offset by the number of subreddits
for user in users:
    bipartite_graph.AddNode(int(user.Index + subreddit_count))
    user_to_node_id[user.name] = user.Index + subreddit_count

# Add the edges

# this is the simplest way to say an author and a user are connected.
for comment in comments:
    subreddit_node_id = get_node_id_by_subreddit_id(comment.subreddit_id)
    user_node_id = get_node_id_by_author(comment.author)

    if subreddit_node_id != None and user_node_id != None:
        bipartite_graph.AddEdge(int(subreddit_node_id), int(user_node_id))

# TODO alternative ways to decide if user and subreddit are connected

print 'Nodes: ' + str(bipartite_graph.GetNodes())
print 'Edges: ' + str(bipartite_graph.GetEdges())

print 'Saving binary'
FOut = snap.TFOut("graphs/bipartite_connected_by_comment.graph")
bipartite_graph.Save(FOut)
FOut.Flush()
