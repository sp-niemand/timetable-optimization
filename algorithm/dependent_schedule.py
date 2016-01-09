"""
Составление расписаний для зависимых задач
"""

import algorithm.schedule as at
import algorithm.dependency as ad
from classes.schedule import Schedule, Task
from algorithm.dependency import NotDirectedAcyclicGraph
from classes.exception import BaseException as BException


class NoOptimalSchedule(BException):
    pass


def validate_dependency_graph(dependency_graph, task_costs):
    """
    Проверяет, нет ли в графе зависимостей задач, которые не описаны
    в матрице task_costs. Также добавляет в граф зависимостей задачи,
    которых там не хватает

    :param networkx.DiGraph dependency_graph:
    :param numpy.matrix task_costs:
    :rtype None|str
    :return: None if no errors or error message if there is some
    """
    _, task_count = task_costs.shape
    tasks = set(range(0, task_count))
    dependency_graph_tasks = set(dependency_graph.nodes())
    redundant_tasks = dependency_graph_tasks.difference(tasks)
    if redundant_tasks:
        return "Redundant tasks in dependency graph: {}".format(str(redundant_tasks))
    dependency_graph.add_nodes_from(tasks.difference(dependency_graph_tasks))
    return None


def get_optimal_schedule(task_costs, dependency_graph, export_intermediate_results = False):
    """
    Возвращает расписание для зависимых задач

    :param numpy.matrix task_costs:
    :param networkx.DiGraph dependency_graph:
    :param bool export_intermediate_results:
    :return:
    :raises NoOptimalSchedule If failed to calculate optimal schedule
    """
    processor_count, _ = task_costs.shape
    result = Schedule(list(range(0, processor_count)))
    try:
        # обходим граф зависимости по уровням
        for (level, tasks) in ad.iterate_levels(dependency_graph):
            # составление подматрицы для уровня тасок
            stage_schedule = at.get_optimal_schedule(task_costs[:, tasks],
                                                     export_intermediate_results=True,
                                                     export_file_name_prefix='level{}_'.format(level))
            # переименование тасков правильно
            for proc, items in stage_schedule:
                for item in items:
                    if isinstance(item, Task):
                        item.name = tasks[item.name]
            result.concat(stage_schedule)
    except NotDirectedAcyclicGraph:
        raise NoOptimalSchedule('Dependency graph is not a directed acyclic graph')

    return result
