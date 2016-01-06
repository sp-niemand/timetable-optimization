from networkx.readwrite.adjlist import read_adjlist
import networkx as nx
import numpy as np
from classes.exception import BaseException as BException


class InvalidTaskParameters(BException):
    pass


def read_task_dependency_graph(path):
    """
    :param str path: file to read dependency graph from
    :rtype nx.DiGraph
    :return: task dependency graph
    :exception FileNotFoundError If file not found
    """
    base_graph = nx.DiGraph()
    return read_adjlist(path, create_using=base_graph, nodetype=int)


def read_task_parameters(path):
    """
    :param str path: CSV-formatted file to read task parameters from
    :rtype np.matrix
    :return: task parameters matrix
    :raises InvalidTaskParameters If something's wrong in the file
    """
    with open(path) as f:
        try:
            result = [
                [int(x.strip()) for x in row.split(',')]
                for row in f if row.strip() != ''
            ]
        except ValueError as e:
            raise InvalidTaskParameters('Error encountered while reading from task parameters file: ' + str(e))
    return np.matrix(result, np.uint)
