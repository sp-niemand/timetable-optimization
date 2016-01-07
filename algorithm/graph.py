"""
Общие алгоритмы работы с графами
"""

import networkx as nx
from networkx.algorithms.flow.utils import build_residual_network
from networkx.algorithms.shortest_paths.weighted import _dijkstra


def successive_shortest_path(network, source, sink):
    """
    Successive Shortest Path max flow min cost algo

    https://www.topcoder.com/community/data-science/data-science-tutorials/minimum-cost-flow-part-two-algorithms/

    :param networkx.DiGraph network:
    :param str source:
    :param str sink:
    :rtype dict|None
    :return:
    """

    def _cost_optimal_augmenting_path(graph, source, target):
        """
        Возвращает оптимальный увеличивающий путь, используя
        алгоритм Дейкстры
        :param graph:
        :param source:
        :param target:
        :return:
        """
        paths = {source: [source]}
        (length, path) = _dijkstra(graph, source, target=target, paths=paths, get_weight=lambda u, v, edata:
             None if edata.get('capacity') <= 0 else edata.get('cost'))
        if target not in path:
            raise nx.NetworkXNoPath
        return path[target]

    def _augment_flow(graph, path, flow_diff):
        """
        Увеличивает поток по заданному увеличивающему пути на значение flow_diff
        :param graph:
        :param path:
        :param flow_diff:
        :return:
        """
        for u, v in zip(path[:-1], path[1:]):
            graph[u][v]['capacity'] = graph[u][v]['capacity'] - flow_diff
            graph[v][u]['capacity'] = graph[v][u]['capacity'] + flow_diff

    def _build_residual_network(network):
        """
        Строит остаточную сеть для заданной сети
        :param network:
        :return:
        """
        result = build_residual_network(network, 'capacity')
        # add costs for residual edges using their original counterparts
        for u, v, cost in network.edges_iter(data='cost'):
            result[u][v]['cost'] = cost
            result[v][u]['cost'] = -cost
        return result

    def _reduce_cost(residual_network, network, potentials):
        """
        Модифицирует стоимости ребёр, чтобы в остаточной сети не было ребер с
        отрицательной стоимостью
        :param residual_network:
        :param network:
        :param potentials:
        :return:
        """
        for u, v, cost in network.edges_iter(data='cost'):
            residual_network[u][v]['cost'] = cost + potentials[u] - potentials[v]
            residual_network[v][u]['cost'] = 0

    def _remove_2cycles_in_residual_network(graph):
        """
        Удаление 2-циклов с заменой их на одно рёбро, capacity которого
        равно разнице capacity составляющих 2-цикла, а направлено ребро в сторону,
        в которую была направлена большая из его составляющих
        :param graph:
        :return:
        """
        for u in residual_network.nodes_iter():
            for v in residual_network.successors(u):
                if not residual_network.has_edge(v, u):
                    continue
                merged_cost = residual_network[v][u]['capacity'] - residual_network[u][v]['capacity']
                if merged_cost > 0:
                    residual_network[u][v]['capacity'] = merged_cost
                    del residual_network[v][u]
                elif merged_cost < 0:
                    residual_network[v][u]['capacity'] = -merged_cost
                    del residual_network[u][v]
                else:
                    del residual_network[u][v], residual_network[v][u]

    def _residual_network_to_flow_dict(residual_network):
        """
        Собирает по остаточной сети данные, необходимые для расшифровки
        в результирующее расписание
        :param residual_network:
        :return:
        """
        result = {}
        for u, v, capacity in residual_network.edges_iter(data='capacity'):
            if capacity == 0:
                continue
            if u not in result:
                result[u] = {}
            result[u][v] = capacity
        return result

    residual_network = _build_residual_network(network)
    node_potentials = nx.bellman_ford(network, source, weight='cost')[1]
    _reduce_cost(residual_network, network, node_potentials)

    while True:
        # TODO: maybe we must recalculate node_potentials on every iteration
        try:
            augmenting_path = _cost_optimal_augmenting_path(residual_network, source, sink)
        except nx.NetworkXNoPath:
            break
        _reduce_cost(residual_network, network, node_potentials)
        _augment_flow(residual_network, augmenting_path, 1)

    _remove_2cycles_in_residual_network(residual_network)
    return _residual_network_to_flow_dict(residual_network)

if __name__ == '__main__':
    g = nx.DiGraph()
    g.add_edges_from([
        ('s', 1, {'capacity': 5, 'cost': 0}),
        (1, 2, {'capacity': 7, 'cost': 1}),
        (1, 3, {'capacity': 7, 'cost': 5}),
        (2, 3, {'capacity': 2, 'cost': -2}),
        (2, 4, {'capacity': 3, 'cost': 8}),
        (3, 4, {'capacity': 3, 'cost': -3}),
        (3, 5, {'capacity': 2, 'cost': 4}),
        (4, 't', {'capacity': 3, 'cost': 0}),
        (5, 't', {'capacity': 2, 'cost': 0}),
    ])
    print(successive_shortest_path(g, 's', 't'))
