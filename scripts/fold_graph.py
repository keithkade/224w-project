"""
Folds the gaph, based on our hw assignment

author: kade
"""

import snap
import ast
from itertools import combinations

import sys
sys.path.append('scripts/')

from subreddits import get_filtered_subreddits
from users import users
from settings import subreddit_subscriber_cutoff

subreddits = get_filtered_subreddits(subreddit_subscriber_cutoff)

graph_to_fold = 'graphs/bipartite_connected_by_comment.graph'
folded_grph_str = 'graphs/bipartite_connected_by_comment_folded.graph'

FIn = snap.TFIn(graph_to_fold)
graph_to_fold = snap.TUNGraph.Load(FIn)

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

  # connect all subreddits where the same user commented in both
  for user in users:
      user_node = graph_to_fold.GetNI(int(info_to_node_id[user.name]))
      neighbors = []
      for neighbor_id in user_node.GetOutEdges():
          neighbors.append(neighbor_id)
      comb = combinations(neighbors, 2)
      for pair in list(comb):
        # folded_graph.AddEdge(int(pair[0]), int(pair[1]))
        sorted_pair = str(sorted([int(pair[0]), int(pair[1])]))
        if sorted_pair in shared_commenter_counts:
          shared_commenter_counts[sorted_pair] += 1
        else:
          shared_commenter_counts[sorted_pair] = 1

  # Only connect nodes if there are at least N shared commenters
  N = 8
  for pair in shared_commenter_counts:
    if shared_commenter_counts[pair] >= N:
      pair_arr = ast.literal_eval(pair)
      folded_graph.AddEdge(pair_arr[0], pair_arr[1])

  # print shared_commenter_counts
  # folded_graph.AddEdge(int(pair[0]), int(pair[1]))

  print 'Saving graph'
  FOut = snap.TFOut(folded_grph_str)
  folded_graph.Save(FOut)
  FOut.Flush()

def get_jaccard(g, node_id):
  target = g.GetNI(node_id)
  similar = []
  for node in g.Nodes():
    union = set()
    for n in target.GetOutEdges():
      union.add(n)
    for n in node.GetOutEdges():
      union.add(n)

    if len(union) == 0:
      similar.append((0, node_id_to_info[node.GetId()]))
      continue

    Nbrs = snap.TIntV()
    snap.GetCmnNbrs(g, node_id, node.GetId(), Nbrs)
    similar.append((float(Nbrs.Len()) / float(len(union)), node_id_to_info[node.GetId()]))

  return sorted(similar, reverse = True)[0:6]

fold_graph()
FIn = snap.TFIn(folded_grph_str)
folded_graph = snap.TUNGraph.Load(FIn)

print 'Folded Graph Nodes: ' + str(folded_graph.GetNodes())
print 'Folded Graph Edges: ' + str(folded_graph.GetEdges())

# t5_2cneq - politics subreddit - ~100 comments in the subset

# print map(lambda info: info[1]['name'], get_jaccard(folded_graph, int(info_to_node_id['t5_2cneq'])))

# Save edgelist, because it's easier to read it in in networkx
snap.SaveEdgeList(folded_graph, 'graphs/bipartite_connected_by_comment_folded_edgelist.txt')
