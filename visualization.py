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


def write_timetable(timetable, task_costs, path=None):
    """
    :param list[list[int]] timetable:
    :param numpy.matrix task_costs:
    :param str|None path:
    :return:
    """
    result = '\n'.join((str(x) for x in timetable))
    if path:
        with open(path, 'w') as f:
            f.write('Timetable time = {}\n'.format(at.calculate_mean_weighted_flow_time(timetable, task_costs)))
            f.write(result)
    else:
        print('Timetable time = {}'.format(at.calculate_mean_weighted_flow_time(timetable, task_costs)))
        print(result)
