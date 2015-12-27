import networkx as nx
from itertools import groupby


def get_node_levels(graph):
    """
    Adds attribute "level" for each node, which represents it's level in
    the graph if is topologically sorted

    :param nx.DiGraph graph:
    :rtype dict
    :returns {<node>: <level>, ...}
    """
    levels = {k: 0 for k in graph.nodes_iter()}
    for node in nx.topological_sort(graph):
        for successor in graph.successors_iter(node):
            successor_level_candidate = levels[node] + 1
            if levels[successor] < successor_level_candidate:
                levels[successor] = successor_level_candidate
    return levels


def iterate_levels(graph):
    """
    Returns iterator which yields (level, nodes iterable) tuple on each iteration

    :param nx.DiGraph graph:
    :return: iterator
    """
    def _level(node_level_tuple):
        return node_level_tuple[1]
    node_levels = get_node_levels(graph)
    sorted_nodes = sorted(node_levels.items(), key=_level)
    for level, node_iter in groupby(sorted_nodes, key=_level):
        yield (level, (node for node, _ in node_iter))
