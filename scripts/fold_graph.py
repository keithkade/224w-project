"""
Folds the gaph, based on our hw assignment

author: kade
"""

import snap
from itertools import combinations

from subreddits import subreddits
from users import users

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
      folded_graph.AddNode(key)
      nodes_list.append(key)

  # connect all subreddits where the same user commented in both
  for user in users:
      user_node = graph_to_fold.GetNI(info_to_node_id[user.name])
      neighbors = []
      for neighbor_id in user_node.GetOutEdges():
          neighbors.append(neighbor_id)
      comb = combinations(neighbors, 2)
      for pair in list(comb):
          folded_graph.AddEdge(pair[0], pair[1])

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

    Nbrs = snap.TIntV()
    snap.GetCmnNbrs(g, node_id, node.GetId(), Nbrs)
    similar.append((float(Nbrs.Len()) / float(len(union)), node_id_to_info[node.GetId()]))

  return sorted(similar, reverse = True)[0:6]

# fold_graph()
FIn = snap.TFIn(folded_grph_str)
folded_graph = snap.TUNGraph.Load(FIn)

# t5_2cneq - politics subreddit - ~100 comments in the subset

print map(lambda info: info[1]['name'], get_jaccard(folded_graph, info_to_node_id['t5_2cneq']))
