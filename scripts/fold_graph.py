"""
Folds the gaph, based on our hw assignment

author: kade
"""

import snap
from subreddits import subreddits
from users import users

FIn = snap.TFIn("graphs/bipartite_connected_by_comment.graph")
folded_graph = snap.TUNGraph.Load(FIn)

# TODO 
