from networkx import write_graphml
import os.path


path = None


def export_graph(g, file_name):
    """
    Экспортирует граф в формате GraphML

    :param networkx.Graph g:
    :param str file_name:
    :return:
    """
    if path:
        write_graphml(g, os.path.join(path, file_name + '.graphml'))
