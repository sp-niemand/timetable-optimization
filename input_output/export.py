from networkx import write_graphml, write_adjlist
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


def export_dependency_graph(g, file_name):
    """
    Экспортирует граф зависимостей в формате "списки смежности"
    :param networkx.DiGraph g:
    :param str path:
    :return:
    """
    write_adjlist(g, os.path.join(path, file_name + '.txt'))
