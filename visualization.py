import numpy as np
import networkx as nx


def write_graph(graph, path):
    """
    :param nx.Graph graph:
    :param str path:
    """
    nx.write_adjlist(graph, path)


def write_matrix(matrix, path):
    """
    :param np.matrix matrix:
    :param str path:
    """
    with open(path, 'w') as f:
        for row in matrix:
            f.write(','.join([str(x) for x in row.tolist()]) + '\n')
