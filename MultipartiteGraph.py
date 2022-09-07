from networkx import *
from itertools import *
from random import sample
import numpy as np
from more_itertools import pairwise

class MultipartiteGraoh:

    def __init__(self):
        self.G = Graph()
        
    def random_multipartite_graph(self, subset_sizes, densities):
        if len(subset_sizes) == 0:
            return self.G
        self.subset_sizes = subset_sizes
        self.densities = densities
        # set up subsets of nodes
        try:
            #extents = itertools.pairwise(itertools.accumulate((0,) + subset_sizes))
            extents = pairwise(itertools.accumulate((0,) + subset_sizes))
            subsets = [range(start, end) for start, end in extents]
        except TypeError:
            subsets = subset_sizes

        # add nodes with subset attribute
        # while checking that ints are not mixed with iterables
        try:
            for (i, subset) in enumerate(subsets):
                self.G.add_nodes_from(subset, subset=i)
        except TypeError as err:
            raise NetworkXError("Arguments must be all ints or all iterables") from err

        # Across subsets, all nodes should be adjacent.
        # We can use itertools.combinations() because undirected.
        i, j = 0, 1
        for subset1, subset2 in itertools.combinations(subsets, 2):
            density = densities[i][j]
            #print(i, j)
            j = j + 1
            if j % len(subsets) == 0:
                i = i + 1
                j = i + 1
            #edges_gen = random_edges(subset1, subset2, density)
            #print(edges_gen)
            #for ele in edges_gen:
            #    print(ele)
            #print(list(edges_gen))
            #a = [edge for edge in random_edges(subset1, subset2, density)]
            #print(a)
            #G.add_edges_from(a[0])
            self.G.add_edges_from(list(random_edges(subset1, subset2, density))[0])
        return self.G
    
    def draw_partite_graph(self, label):
        pos = {}
        nodes = self.G.nodes()
        for i in range(len(self.subset_sizes)):
            tmp_nodes = set([n for n in nodes if  self.G.nodes[n]['subset']==i])
            pos.update( (n, (i, j)) for j, n in enumerate(tmp_nodes) )
        nx.draw(self.G, pos=pos, with_labels=label)

    def sub_partite(self, partites):
        partites = set(partites)
        nodes = self.G.nodes()
        tmp_nodes = [n for n in nodes if self.G.nodes[n]["subset"] in partites]
        return self.G.subgraph(tmp_nodes)
