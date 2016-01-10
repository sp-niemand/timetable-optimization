"""
Функционал ввода данных
"""

from networkx.readwrite.adjlist import read_adjlist
import networkx as nx
import numpy as np
from classes.exception import BaseException as BException
import random

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
        return np.matrix(result, np.uint)
    except:
        raise InvalidTaskParameters('Error encountered while reading task parameters file')


def random_dependency_graph(tasks, level_count, max_tasks_on_level):
    """
    Генерирует случайный граф зависимостей
    :param list tasks: Список задач, для которых формируется граф
    :param int level_count: Количество уровней зависимостей
    :param int max_tasks_on_level: Максимальное количество задач на уровне
    :rtype networkx.DiGraph
    :return:
    """
    remaining_tasks = tasks.copy()
    min_tasks_on_level = max(max_tasks_on_level // 2, 1)
    result = nx.DiGraph()
    for level in range(0, level_count):
        level_task_count = random.randint(min_tasks_on_level, max_tasks_on_level)
        level_tasks = remaining_tasks[:level_task_count]
        remaining_tasks = remaining_tasks[level_task_count:]
        if level == 0:
            result.add_nodes_from(level_tasks)
        else:
            current_nodes = result.nodes()
            new_edges = [(random.choice(current_nodes), new_task) for new_task in level_tasks]
            result.add_nodes_from(level_tasks)
            result.add_edges_from(new_edges)
    return result


def random_task_parameters(processor_count, task_count, max_task_time):
    """
    Генерирует случайную матрицу параметров задач
    :param int processor_count:
    :param int task_count:
    :param int max_task_time:
    :rtype numpy.matrix
    :return:
    """
    return np.asmatrix(np.random.random_integers(
            1, max_task_time, processor_count * task_count).reshape(
            (processor_count, task_count)))
