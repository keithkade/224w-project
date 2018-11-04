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
folded_graph = snap.TUNGraph.Load(FIn)

node_id_to_info = {}

subreddit_count = len(subreddits)
user_count      = len(users)

for subreddit in subreddits:
    node_id_to_info[subreddit.Index] = { 'type': 'subreddit', 'id': subreddit.base36_id }

for user in users:
    node_id_to_info[user.Index + subreddit_count] = { 'type': 'user', 'id': user.name }

def fold_graph():
  print 'Folding graph'
  folded_graph = snap.TUNGraph.New()
  nodes_list = []

  # add all the subreddits to the new graph
  for key in node_id_to_info:
    if node_id_to_info[key]['type'] == 'subreddit':
      folded_graph.AddNode(key)
      nodes_list.append(key)

  # get all possible pairs of subreddits
  comb = combinations(nodes_list, 2)

  print str(len(list(comb))) + ' combinations to check'

  for pair in list(comb):
    Nbrs = snap.TIntV()
    snap.GetCmnNbrs(graph, pair[0], pair[1], Nbrs)
    # if the two subreddits have a user in common, connect them
    if Nbrs.Len() > 0:
      folded_graph.AddEdge(pair[0], pair[1])

  print 'Saving graph'
  FOut = snap.TFOut(folded_grph_str)
  folded_graph.Save(FOut)
  FOut.Flush()

  return folded_graph

folded_graph = fold_graph()

print 'Nodes: ' + str(folded_graph.GetNodes())
print 'Edges: ' + str(folded_graph.GetEdges())
