import algorithm.timetable as at
import algorithm.dependency as ad

def get_optimal_timetable(task_costs, dependency_graph):
    """

    :param numpy.matrix task_costs:
    :param networkx.DiGraph dependency:
    :return:
    """
    for (level, tasks) in ad.iterate_levels(dependency_graph):
        # [0,3,4]
        subtimetable = at.get_optimal_timetable(task_costs[:, tasks])
        for processor_tasks in subtimetable:
            processor_tasks