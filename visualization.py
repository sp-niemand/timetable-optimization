import numpy as np
import networkx as nx
import algorithm.timetable as at


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


def write_timetable(timetable, path=None):
    """
    :param classes.timetable.Timetable timetable:
    :param str|None path:
    :return:
    """
    message = 'Total flow time = {}\n{}'.format(timetable.total_flow_time(), str(timetable))
    if path:
        with open(path, 'w') as f:
            f.write(message)
    else:
        print(message)
