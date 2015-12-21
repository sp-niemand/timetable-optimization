from networkx.readwrite.adjlist import write_adjlist


def write_graph(graph, path):
    """
    :param networkx.Graph graph:
    :param str path:
    """
    write_adjlist(graph, path)


def write_matrix(matrix, path):
    """
    :param list[list[int]] matrix:
    :param str path:
    """
    with open(path, 'w') as f:
        for row in matrix:
            f.write(','.join([str(x) for x in row]))
            f.write('\n')
