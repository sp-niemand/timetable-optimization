import algorithm.timetable as at
import algorithm.dependency as ad
from classes.timetable import Timetable, Task


def get_optimal_timetable(task_costs, dependency_graph):
    """
    :param numpy.matrix task_costs:
    :param networkx.DiGraph dependency_graph:
    :return:
    """
    processor_count, _ = task_costs.shape
    result = Timetable(list(range(0, processor_count)))
    for (level, tasks) in ad.iterate_levels(dependency_graph):
        stage_timetable = at.get_optimal_timetable(task_costs[:, tasks])
        for proc, items in stage_timetable:
            for item in items:
                if isinstance(item, Task):
                    item.name = tasks[item.name]
        result.concat(stage_timetable)
    return result
