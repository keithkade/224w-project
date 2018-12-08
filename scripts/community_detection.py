# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 17:35:32 2018

@author: fade7001
"""

from settings import graph_str, remove_trolls, plot_str
import community
import networkx as nx
import matplotlib.pyplot as plt
from subreddits import subreddits

if remove_trolls:
    folded_grph_str = graph_str+'_without_trolls.txt'
    graph_str = graph_str + "_without_trolls"
    plot_str = plot_str + "_without_trolls"
else:
    folded_grph_str = graph_str+'.txt'

weighted = False
directed = False
dimensions = 128
walk_length = 28
num_walks = 10
window_size = 10
workers = 8
no_iter = 1

def read_graph(folded_grph_str):
	'''
	Reads the input network in networkx.
	'''
	if weighted:
		G = nx.read_edgelist(folded_grph_str, nodetype=int, data=(('weight',float),), create_using=nx.DiGraph())
	else:
		G = nx.read_edgelist(folded_grph_str, nodetype=int, create_using=nx.DiGraph())
		for edge in G.edges():
			G[edge[0]][edge[1]]['weight'] = 1

	if not directed:
		G = G.to_undirected()

	return G

nx_G = read_graph(folded_grph_str)

#first compute the best partition
partition = community.best_partition(nx_G)

# Keep the node id to name map
node_id_to_info = {}

subreddit_count = len(subreddits)

for subreddit in subreddits:
    node_id_to_info[subreddit.Index] = { 'type': 'subreddit', 'id': subreddit.base36_id, 'name': subreddit.name }

# Get the labels for the plot 
labels = {}
for node in nx_G.nodes():
    labels[node] = node_id_to_info[node]['name']

#drawing
colors = ["blue", "red", "black", "yellow", "green", "orange"]
size = float(len(set(partition.values())))
pos = nx.spring_layout(nx_G)
label_pos = {key: val + 0.01 for key, val in pos.items()}
count = 0.
for i, com in enumerate(set(partition.values())):
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(nx_G, pos, list_nodes, node_size = 100,
                                node_color = colors[i])

nx.draw_networkx_labels(nx_G,label_pos,labels,font_size=16,font_color='r')
# nx.draw_networkx_labels(nx_G,label_pos,font_size=16,font_color='r')
nx.draw_networkx_edges(nx_G, pos, alpha=0.5)
plt.savefig(plot_str+"._louvain.png", format="PNG")
plt.show()