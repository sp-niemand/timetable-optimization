from networkx.readwrite.adjlist import read_adjlist
import networkx as nx
import numpy as np

def read_task_dependency_graph(path):
    """
    :param str path: file to read dependency graph from
    :rtype nx.DiGraph
    :return: task dependency graph
    :exception FileNotFoundError If file not found
    """
    base_graph = nx.DiGraph()
    return read_adjlist(path, create_using=base_graph)


def read_task_parameters(path):
    """
    :param str path: CSV-formatted file to read task parameters from
    :rtype np.matrix
    :return: task parameters matrix
    """
    with open(path) as f:
        result = [
            [int(x) for x in row.split(',')]
            for row in f if row.strip() != ''
        ]
    return np.matrix(result, np.uint)
