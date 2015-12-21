from networkx.readwrite.adjlist import read_adjlist
from networkx import DiGraph

def read_task_dependency_graph(path):
    '''
    :param path: file to read dependency graph from
    :return: task dependency graph
    '''
    result = DiGraph()
    return read_adjlist(path, create_using=result)