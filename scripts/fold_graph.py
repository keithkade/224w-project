"""
Folds the gaph, based on our hw assignment

author: kade
"""

import snap
import ast
import os
import pandas as pd
from itertools import combinations

import sys
sys.path.append('scripts/')

from subreddits import subreddits
from users import users
from settings import fold_connection_threshold, bipartite_graph_file, graph_str, trolls_csv, remove_trolls

trolls_df = pd.read_csv(trolls_csv)

graph_to_fold = bipartite_graph_file

FIn = snap.TFIn(graph_to_fold)
graph_to_fold = snap.TUNGraph.Load(FIn)
os.remove(bipartite_graph_file)

node_id_to_info = {}
info_to_node_id = {}

subreddit_count = len(subreddits)
user_count      = len(users)

for subreddit in subreddits:
    node_id_to_info[subreddit.Index] = { 'type': 'subreddit', 'id': subreddit.base36_id, 'name': subreddit.name }
    info_to_node_id[subreddit.base36_id] = subreddit.Index

for user in users:
    node_id_to_info[user.Index + subreddit_count] = { 'type': 'user', 'id': user.name }
    info_to_node_id[user.name] = user.Index + subreddit_count

def fold_graph():
  print 'Folding graph'
  folded_graph = snap.TUNGraph.New()
  nodes_list = []

  # add all the subreddits to the new graph
  for key in node_id_to_info:
    if node_id_to_info[key]['type'] == 'subreddit':
      folded_graph.AddNode(int(key))
      nodes_list.append(key)

  shared_commenter_counts = {}

  # connect all subreddits where the same user commented/posted in both
  for user in users:
    if remove_trolls and user.name in trolls_df.name.values:
      continue
    else:
      user_node = graph_to_fold.GetNI(int(info_to_node_id[user.name]))
      neighbors = []
      for neighbor_id in user_node.GetOutEdges():
          neighbors.append(neighbor_id)
      comb = combinations(neighbors, 2)
      for pair in list(comb):

        # manually investigating the link between Conservative and SandersForPresident
        # Conservative: t5_2qh6p
        # SandersForPresident: t5_2zbq7
        # if node_id_to_info[int(pair[0])]['name'] == 'Conservative' and node_id_to_info[int(pair[1])]['name'] == 'SandersForPresident':
        #   print user
        #
        # if node_id_to_info[int(pair[1])]['name'] == 'Conservative' and node_id_to_info[int(pair[0])]['name'] == 'SandersForPresident':
        #   print user

        sorted_pair = str(sorted([int(pair[0]), int(pair[1])]))
        if sorted_pair in shared_commenter_counts:
          shared_commenter_counts[sorted_pair] += 1
        else:
          shared_commenter_counts[sorted_pair] = 1

  # Only connect nodes if there are at least N shared commenters
  N = fold_connection_threshold
  for pair in shared_commenter_counts:
    if shared_commenter_counts[pair] >= N:
      pair_arr = ast.literal_eval(pair)
      folded_graph.AddEdge(pair_arr[0], pair_arr[1])

  # print shared_commenter_counts
  # folded_graph.AddEdge(int(pair[0]), int(pair[1]))

  return folded_graph

folded_graph = fold_graph()

print 'Folded Graph Nodes: ' + str(folded_graph.GetNodes())
print 'Folded Graph Edges: ' + str(folded_graph.GetEdges())

# t5_2cneq - politics subreddit - ~100 comments in the subset

# Save edgelist, because it's easier to read it in in networkx
snap.SaveEdgeList(folded_graph, graph_str+'.txt')
