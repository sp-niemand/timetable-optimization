from networkx.readwrite.adjlist import read_adjlist
from networkx import DiGraph


def read_task_dependency_graph(path):
    """
    :param path: file to read dependency graph from
    :return: task dependency graph
    :exception FileNotFoundError If file not found
    """
    base_graph = DiGraph()
    return read_adjlist(path, create_using=base_graph)


def read_task_parameters(path):
    """
    :param path: CSV-formatted file to read task parameters from
    :return: task parameters matrix
    """
    with open(path) as f:
        result = [
            [int(x) for x in row.split(',')]
            for row in f if row.strip() != ''
        ]
    return result
