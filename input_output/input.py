"""
Функционал ввода данных
"""

from networkx.readwrite.adjlist import read_adjlist
import networkx as nx
import numpy as np
from classes.exception import BaseException as BException


class InvalidTaskParameters(BException):
    pass


class InvalidTaskDependencies(BException):
    pass


def read_task_dependency_graph(path):
    """
    считывает граф зависимостей, на входе строка пути

    :param str path: file to read dependency graph from
    :rtype nx.DiGraph - тип возвращаемого значения
    :return: task dependency graph - описание возвращаемого значения
    :exception FileNotFoundError If file not found
    """
    base_graph = nx.DiGraph()  # konstructor classa sozdaet pustoi graph
    try:
        return read_adjlist(path, create_using=base_graph, nodetype=int)
    except:
        raise InvalidTaskDependencies('Error encountered while reading task dependencies file')


def read_task_parameters(path):
    """
    считывает матрицу времен возвращает двумерный массив
    :param str path: CSV-formatted file to read task parameters from
    :rtype np.matrix
    :return: task parameters matrix
    :raises InvalidTaskParameters If something's wrong in the file
    """
    with open(path) as f:
        try:
            result = [
                [int(x.strip()) for x in row.split(',')]
                for row in f if row.strip() != ''
            ]
        except ValueError as e:
            raise InvalidTaskParameters('Error encountered while reading task parameters file: ' + str(e))
        except:
            raise InvalidTaskParameters('Error encountered while reading task parameters file')
    try:
        return np.matrix(result, np.uint)  # TODO: get rid of numpy.matrix
    except:
        raise InvalidTaskParameters('Error encountered while reading task parameters file')
