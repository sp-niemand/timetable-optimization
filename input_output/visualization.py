"""
Функционал вывода данных (на экран либо в картинку)
"""

import numpy as np
import networkx as nx

# TODO: визуализировать результирующее расписание
# TODO: визуализировать транспортную сеть, созданную для нахождения расписания
# TODO: визуализировать на этой транспортной сети найденный макс. поток


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


def write_schedule(schedule, path=None):
    """
    :param classes.schedule.Schedule schedule:
    :param str|None path:
    :return:
    """
    message = 'Total flow time = {}\n{}'.format(schedule.total_flow_time(), str(schedule))
    if path:
        with open(path, 'w') as f:
            f.write(message)
    else:
        print(message)
