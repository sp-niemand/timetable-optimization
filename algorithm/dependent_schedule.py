import algorithm.schedule as at
import algorithm.dependency as ad
from classes.schedule import Schedule, Task


def get_optimal_schedule(task_costs, dependency_graph):
    """
    :param numpy.matrix task_costs:
    :param networkx.DiGraph dependency_graph:
    :return:
    """
    processor_count, _ = task_costs.shape
    result = Schedule(list(range(0, processor_count)))
    for (level, tasks) in ad.iterate_levels(dependency_graph):
        stage_schedule = at.get_optimal_schedule(task_costs[:, tasks])
        for proc, items in stage_schedule:
            for item in items:
                if isinstance(item, Task):
                    item.name = tasks[item.name]
        result.concat(stage_schedule)
    return result
