"""
This file creates a bipartite graph based on comments.

I also populate a couple maps, user_to_node_id and subreddit_id_to_node_id, for util purposes

@author: kade
"""
import sys
sys.path.append('scripts/')

import pandas as pd
import snap
from settings import subreddit_subscriber_cutoff
from subreddits import get_filtered_subreddits
from users import users
from comments import comments

subreddits = get_filtered_subreddits(subreddit_subscriber_cutoff)

################################################ Globals that get used later

subreddit_id_to_node_id = {}
user_to_node_id = {}
node_id_to_name = {}

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

print 'Adding nodes'

for subreddit in subreddits:
    bipartite_graph.AddNode(int(subreddit.Index))
    subreddit_id_to_node_id[subreddit.base36_id] = subreddit.Index
    node_id_to_name[subreddit.Index] = subreddit.name

# offset by the number of subreddits
for user in users:
    bipartite_graph.AddNode(int(user.Index + subreddit_count))
    user_to_node_id[user.name] = user.Index + subreddit_count
    node_id_to_name[user.Index + subreddit_count] = user.name

# Add the edges

# connect if a user has commented in a subreddit at least n times
def connect_via_n_comment(n):

    user_comment_counts = {}
    for user in users:
        user_comment_counts[user.name] = 0

    comment_counts = {}

    for comment in comments:
        user_comment_counts[comment.author] += 1

    for comment in comments:
        # ignore super active accounts. #TODO figure out better solution
        if user_comment_counts[comment.author] > 100:
            continue

        subreddit_node_id = get_node_id_by_subreddit_id(comment.subreddit_id)
        user_node_id = get_node_id_by_author(comment.author)

        user_comment_counts[comment.author] += 1

        if subreddit_node_id != None and user_node_id != None:
            if (int(subreddit_node_id), int(user_node_id)) in comment_counts:
                comment_counts[(int(subreddit_node_id), int(user_node_id))] += 1
            else:
                comment_counts[(int(subreddit_node_id), int(user_node_id))] = 1

    for subreddit_node_id, user_node_id in comment_counts:
        if comment_counts[(int(subreddit_node_id), int(user_node_id))] >= n:
            bipartite_graph.AddEdge(int(subreddit_node_id), int(user_node_id))

print 'Adding edges'
connect_via_n_comment(1)
# connect_via_n_comment(2)
# connect_via_n_comment(3)

# TODO alternative ways to decide if user and subreddit are connected

print 'Nodes: ' + str(bipartite_graph.GetNodes())
print 'Edges: ' + str(bipartite_graph.GetEdges())

print 'Saving binary'
FOut = snap.TFOut("graphs/bipartite_connected_by_comment.graph")
bipartite_graph.Save(FOut)
FOut.Flush()
