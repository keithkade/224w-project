from settings import should_deconvolve, graph_str, compute_communities

import build_bipartite_graph

import fold_graph

if should_deconvolve:
    import deconvolve

import convert_to_gephi

if compute_communities:
    import community_detection

print graph_str
