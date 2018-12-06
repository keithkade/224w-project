# -*- coding: utf-8 -*-
"""
Created on Sat Nov 03 15:04:48 2018

@author: dimit_000
"""

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
import sys
sys.path.append('scripts/')
from node2vec import *
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from matplotlib import colors
from subreddits import subreddits
import snap

weighted = False
directed = False
dimensions = 128
walk_length = 28
num_walks = 10
window_size = 10
workers = 8
no_iter = 1
graph_input = "graphs/bipartite_connected_by_comment_folded_edgelist.txt"

# Keep the node id to name map
node_id_to_info = {}
for subreddit in subreddits:
    node_id_to_info[subreddit.Index] = {'type': 'subreddit', 'id': subreddit.base36_id, 'name': subreddit.name }

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
# Keep only the largest connected component to run the node2vec model
Gc = max(nx.connected_component_subgraphs(nx_G), key=len)
G = Graph(Gc, directed, p, q)
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

# Fit a kmeans model to the embedded vectors
# X = model[model.wv.vocab]
X = np.empty([Gc.number_of_nodes(), dimensions])
x_labels = []
for i, node_id in enumerate(model.wv.vocab.keys()):
    X[i,:] = model[node_id]
    x_labels.append(str(node_id_to_info[int(node_id)]['name']))

kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
label = kmeans.labels_

# fit a 2d PCA model to the vectors
pca = PCA(n_components=2)
pca_Y = pca.fit_transform(X)
# create a scatter plot of the projection
color = ['red','blue']
# Change figure size
fig_size = plt.rcParams["figure.figsize"]
print "Current size:", fig_size
fig_size[0] = 40
fig_size[1] = 40
plt.rcParams["figure.figsize"] = fig_size
print "Current size:", fig_size

# Plot clustered nodes on the projected PCA data
for i in range(pca_Y.shape[0]):
    x = pca_Y[i][0]
    y = pca_Y[i][1]
    plt.plot(x, y, marker = "o", c=color[label[i]], markersize = 20)
    plt.text(x * (1 + 0.01), y * (1 + 0.01) , x_labels[i], fontsize=20)
plt.xlim([pca_Y[:, 0].min()-0.1, pca_Y[:, 0].max()+0.1])
plt.ylim([pca_Y[:, 1].min()-0.1, pca_Y[:, 1].max()+0.1])
plt.savefig("/plots/pca_plot.png")
plt.show()


# Try TSNE instead of PCA
tsne = TSNE(n_components=2, init='pca', random_state=0)
tsne_Y = tsne.fit_transform(X)
for i in range(tsne_Y.shape[0]):
    x = tsne_Y[i][0]
    y = tsne_Y[i][1]
    plt.plot(x, y, marker = "o", c=color[label[i]], markersize = 20)
    plt.text(x * (1 + 0.01), y * (1 + 0.01) , x_labels[i], fontsize=20)
plt.xlim([tsne_Y[:, 0].min()-0.1, tsne_Y[:, 0].max()+0.1])
plt.ylim([tsne_Y[:, 1].min()-0.1, tsne_Y[:, 1].max()+0.1])
# plt.savefig("/plots/tsne_plot.png")
plt.show()
