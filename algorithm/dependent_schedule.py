import algorithm.schedule as at
import algorithm.dependency as ad
from classes.schedule import Schedule, Task
from algorithm.dependency import NotDirectedAcyclicGraph
from classes.exception import BaseException as BException


class NoOptimalSchedule(BException):
    pass


def validate_dependency_graph(dependency_graph, task_costs):
    """
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


def get_optimal_schedule(task_costs, dependency_graph):
    """
    :param numpy.matrix task_costs:
    :param networkx.DiGraph dependency_graph:
    :return:
    :raises NoOptimalSchedule If failed to calculate optimal schedule
    """
    processor_count, _ = task_costs.shape
    result = Schedule(list(range(0, processor_count)))
    try:
        for (level, tasks) in ad.iterate_levels(dependency_graph):
            stage_schedule = at.get_optimal_schedule(task_costs[:, tasks])
            for proc, items in stage_schedule:
                for item in items:
                    if isinstance(item, Task):
                        item.name = tasks[item.name]
            result.concat(stage_schedule)
    except NotDirectedAcyclicGraph:
        raise NoOptimalSchedule('Dependency graph is not a directed acyclic graph')

    return result
