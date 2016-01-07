"""
Модуль, отвечающий за работу с графом зависимостей
"""

import networkx as nx
from itertools import groupby
from classes.exception import BaseException as BException


class NotDirectedAcyclicGraph(BException):
    pass


def get_node_levels(graph):
    """
    Returns the level of each node in graph

    :param nx.DiGraph graph:
    :rtype dict
    :returns {<node>: <level>, ...}
    :raises NotDirectedAcyclicGraph If dependency graph is not a directed acyclic graph
    """
    levels = {k: 0 for k in graph.nodes_iter()}
    try:
        topological_sort_result = nx.topological_sort(graph)
    except nx.NetworkXUnfeasible:
        raise NotDirectedAcyclicGraph()
    for node in topological_sort_result:
        for successor in graph.successors_iter(node):
            successor_level_candidate = levels[node] + 1
            if levels[successor] < successor_level_candidate:
                levels[successor] = successor_level_candidate
    return levels


def iterate_levels(graph):
    """
    Returns iterator which yields (level, nodes list) tuple on each iteration

    Возвращает итератор, который на каждой итерации по нему выдаёт пару (номер уровня, список вершин)

    :param nx.DiGraph graph:
    :return: iterator
    :raises NotDirectedAcyclicGraph If dependency graph is not a directed acyclic graph
    """
    def _level(node_level_tuple):
        return node_level_tuple[1]
    node_levels = get_node_levels(graph)
    sorted_nodes = sorted(node_levels.items(), key=_level)
    for level, node_iter in groupby(sorted_nodes, key=_level):
        yield (level, list(map(lambda x: x[0], node_iter)))
