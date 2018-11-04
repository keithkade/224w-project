# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 15:04:48 2018

@author: dimit_000
"""

os.chdir("G:\\Docs\\Stanford - Mining Massive Datasets\\CS224w\\Project")
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 15:48:36 2018

@author: dimit_000
"""
import networkx as nx
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
import networkx as nx
from node2vec import *
from gensim.models import Word2Vec

weighted = False
directed = False
dimensions = 128
walk_length = 28
num_walks = 10
window_size = 10
workers = 8
no_iter = 1
graph_input = "graphs/bipartite_connected_by_comment_folded_edgelist.txt"

def read_graph():
	'''
	Reads the input network in networkx.
	'''
	if weighted:
		G = nx.read_edgelist(graph_input, nodetype=int, data=(('weight',float),), create_using=nx.DiGraph())
	else:
		G = nx.read_edgelist(graph_input, nodetype=int, create_using=nx.DiGraph())
		for edge in G.edges():
			G[edge[0]][edge[1]]['weight'] = 1

	if not directed:
		G = G.to_undirected()

	return G

def learn_embeddings(walks):
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''
	walks = [map(str, walk) for walk in walks]
	model = Word2Vec(walks, size=dimensions, window = window_size, min_count=0, sg=1, workers = workers, iter = no_iter)
	# model.wv.save_word2vec_format(output)
	# model.wv.save_word2vec_format(output, binary=False)
	return model

# For now, node2vec will actually be equivelant to the deepwalk model 
p, q = 1, 1
nx_G = read_graph()
G = Graph(nx_G, directed, p, q)
G.preprocess_transition_probs()
walks = G.simulate_walks(num_walks, walk_length)
model = learn_embeddings(walks)
# summarize the loaded model
# model = Word2Vec.load(output)
print(model)

# summarize nodes
nodes = list(model.wv.vocab)
print(nodes)
# access vector for one node
print(model['9076'])

# Look up top 5 most similar nodes to '9076'
node_id = ['9076']
model.wv.most_similar(positive = node_id, topn = 5)
# [('34', 0.9948307871818542),
#  ('16', 0.9929938316345215),
#  ('31', 0.9839209318161011),
#  ('23', 0.9677373766899109),
#  ('24', 0.9609790444374084)]



# fit a 2d PCA model to the vectors
X = model[model.wv.vocab]
pca = PCA(n_components=2)
result = pca.fit_transform(X)
# create a scatter plot of the projection
plt.scatter(result[:, 0], result[:, 1])
plt.xlim([-1.6, 3.5])
plt.ylim([-1.6, 1.8])
# for i, node_id in enumerate(nodes):
# 	plt.annotate(node_id, xy=(result[i, 0], result[i, 1]))
plt.show()