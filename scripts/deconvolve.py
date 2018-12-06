# -*- coding: utf-8 -*-
"""
Created on Sat Dec 01 18:26:42 2018

@author: dimit_000
"""

import numpy as np
import snap
import networkx as nx
import matplotlib.pyplot as plt
import os

from settings import graph_str, show_networkx_deconvolved

folded_grph_str = graph_str+'.txt'
folded_graph = snap.LoadEdgeList(snap.PNGraph, folded_grph_str, 0, 1)
os.remove(folded_grph_str)

node_id_to_adj = {}
adj_to_node_id = {}
for adj_node_id, node in enumerate(folded_graph.Nodes()):
    node_id = node.GetId()
    node_id_to_adj[node_id] = adj_node_id
    adj_to_node_id[adj_node_id] = node_id

def get_adjacency_matrix(Graph):
    '''
    This function might be useful for you to build the adjacency matrix of a
    given graph and return it as a numpy array
    '''
    ##########################################################################
    #TODO: Your code here
    no_nodes = Graph.GetNodes()
    adjacency_matrix = np.zeros(shape=(no_nodes, no_nodes))
    for node in Graph.Nodes():
        node_id = node.GetId()
        for neighbor_id in node.GetOutEdges():
            adjacency_matrix[node_id_to_adj[node_id]][node_id_to_adj[neighbor_id]] += 1
    return adjacency_matrix
    ##########################################################################

adj_matrix = get_adjacency_matrix(folded_graph)


def ND(mat,beta=0.99,alpha=1,control=0):
    '''
    This is a python implementation/translation of network deconvolution by MIT-KELLIS LAB


     LICENSE: MIT-KELLIS LAB


     AUTHORS:
        Algorithm was programmed by Soheil Feizi.
        Paper authors are S. Feizi, D. Marbach,  M. M?©dard and M. Kellis
    Python implementation: Gideon Rosenthal

    REFERENCES:
       For more details, see the following paper:
        Network Deconvolution as a General Method to Distinguish
        Direct Dependencies over Networks
        By: Soheil Feizi, Daniel Marbach,  Muriel Médard and Manolis Kellis
        Nature Biotechnology

    --------------------------------------------------------------------------
     ND.m: network deconvolution
    --------------------------------------------------------------------------

    DESCRIPTION:

     USAGE:
        mat_nd = ND(mat)
        mat_nd = ND(mat,beta)
        mat_nd = ND(mat,beta,alpha,control)


     INPUT ARGUMENTS:
     mat           Input matrix, if it is a square matrix, the program assumes
                   it is a relevance matrix where mat(i,j) represents the similarity content
                   between nodes i and j. Elements of matrix should be
                   non-negative.
     optional parameters:
     beta          Scaling parameter, the program maps the largest absolute eigenvalue
                   of the direct dependency matrix to beta. It should be
                   between 0 and 1.
     alpha         fraction of edges of the observed dependency matrix to be kept in
                   deconvolution process.
     control       if 0, displaying direct weights for observed
                   interactions, if 1, displaying direct weights for both observed and
                   non-observed interactions.

     OUTPUT ARGUMENTS:

     mat_nd        Output deconvolved matrix (direct dependency matrix). Its components
                   represent direct edge weights of observed interactions.
                   Choosing top direct interactions (a cut-off) depends on the application and
                   is not implemented in this code.

     To apply ND on regulatory networks, follow steps explained in Supplementary notes
     1.4.1 and 2.1 and 2.3 of the paper.
     In this implementation, input matrices are made symmetric.

    **************************************************************************
     loading scaling and thresholding parameters
    '''
    import scipy.stats.mstats as stat
    from numpy import linalg as LA


    if beta>=1 or beta<=0:
        print 'error: beta should be in (0,1)'

    if alpha>1 or alpha<=0:
            print 'error: alpha should be in (0,1)';


    '''
    ***********************************
     Processing the inut matrix
     diagonal values are filtered
    '''
    np.fill_diagonal(mat, 0)
    mat_th = mat
    '''
    ***********************************
    eigen decomposition
    '''
    print 'Decomposition and deconvolution...'

    Dv,U = LA.eigh(mat_th)
    D = np.diag((Dv))
    lam_n=np.abs(np.min(np.min(np.diag(D)),0))
    lam_p=np.abs(np.max(np.max(np.diag(D)),0))


    m1=lam_p*(1-beta)/beta
    m2=lam_n*(1+beta)/beta
    m=max(m1,m2)

    #network deconvolution
    for i in range(D.shape[0]):
        D[i,i] = (D[i,i])/(m+D[i,i])

    mat_new1 = np.dot(U,np.dot(D,LA.inv(U)))


    '''

    ***********************************
     displying direct weights
    '''
    if control==0:
        ind_edges = (mat_th>0)*1.0;
        ind_nonedges = (mat_th==0)*1.0;
        m1 = np.max(np.max(mat*ind_nonedges));
        m2 = np.min(np.min(mat_new1));
        mat_new2 = (mat_new1+np.max(m1-m2,0))*ind_edges+(mat*ind_nonedges);
    else:
        m2 = np.min(np.min(mat_new1));
        mat_new2 = (mat_new1+np.max(-m2,0));


    '''
    ***********************************
     linearly mapping the deconvolved matrix to be between 0 and 1
    '''
    m1 = np.min(np.min(mat_new2));
    m2 = np.max(np.max(mat_new2));
    mat_nd = (mat_new2-m1)/(m2-m1);


    return mat_nd

deconvolved_adj_matrix = ND(adj_matrix,beta=0.99,alpha=1,control=0)

y = 0.63
th = deconvolved_adj_matrix>=y
deconvolved_adj_matrix=deconvolved_adj_matrix*th;
deconvolved_adj_matrix = np.where(deconvolved_adj_matrix==0, 0, 1)

deconvolved_folded_graph = snap.TNGraph.New()
nodes = node_id_to_adj.keys()
for node_id in nodes:
   deconvolved_folded_graph.AddNode(node_id)

for edge_point1 in range(deconvolved_adj_matrix.shape[0]):
    for edge_point2 in range(deconvolved_adj_matrix.shape[0]):
        if deconvolved_adj_matrix[edge_point1][edge_point2] == 1:
            node1_id = adj_to_node_id[edge_point1]
            node2_id = adj_to_node_id[edge_point2]
            if not deconvolved_folded_graph.IsEdge(node1_id, node2_id):
                deconvolved_folded_graph.AddEdge(node1_id, node2_id)

print 'Deconvolved graph Nodes: ' + str(deconvolved_folded_graph.GetNodes())
print 'Deconvolved graph Edges: ' + str(deconvolved_folded_graph.GetEdges())

snap.SaveEdgeList(deconvolved_folded_graph, folded_grph_str)

if show_networkx_deconvolved:
	weighted = False
	directed = True
	def read_graph(graph_input, weighted):
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

	nx_deconvolved_folded_graph = read_graph(folded_grph_str, weighted)

	plt.figure(figsize=(20,14))

	pos = nx.spring_layout(nx_deconvolved_folded_graph,scale=2)
	nx.draw(nx_deconvolved_folded_graph, pos=pos, node_size=12, node_color='lightblue',
	    linewidths=0.25, font_size=10, font_weight='bold', with_labels=True, dpi=1000)

	plt.show()

	# Show degrees of all nodes
	import operator
	sorted(nx_deconvolved_folded_graph.degree().items(), key=operator.itemgetter(1))
