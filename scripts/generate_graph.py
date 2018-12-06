from settings import should_deconvolve

import build_bipartite_graph
import fold_graph

if should_deconvolve:
    import deconvolve

import convert_to_gephi
