import algorithm.schedule as at
import algorithm.dependency as ad
from classes.schedule import Schedule, Task
from algorithm.dependency import NotDirectedAcyclicGraph
from classes.exception import BaseException as BException

class NoOptimalSchedule(BException):
    pass


def _add_tasks_to_schedule_without_changing_busy_time(schedule, tasks, task_costs, dependency_graph):
    """
    Добавляет задачи в расписании таким образом, чтобы максимальное время выполнения расписания не росло

    :param classes.schedule.Schedule schedule: Расписание, к которому происходит добавление
    :param list[int] tasks: Задачи, которые можно добавить
    :param numpy.matrix task_costs: Матрица стоимостей задач
    :param networkx.DiGraph dependency_graph: Граф зависимостей задач
    :rtype list[int]
    :return: Список задач, которые не удалось добавить
    """

    def _earliest_start_time(task):
        predecessors = dependency_graph.predecessors(task)
        return max(task_flow_times[p] for p in predecessors) if predecessors else 0

    def _branch_and_bound(processor, tasks):
        class SolutionNode:
            def __init__(self, schedule, remaining_tasks):
                self.schedule = schedule
                self.remaining_tasks = remaining_tasks.copy()
                self.total_flow_time = schedule.total_flow_time()
                self.busy_time = schedule.max_busy_time()

            def is_better_than(self, other):
                return self.busy_time > other.busy_time or (
                    self.busy_time == other.busy_time and self.total_flow_time < other.total_flow_time)

        interval_start = schedule.busy_time(processor)
        interval_finish = max_busy_time
        first_node = SolutionNode(Schedule([processor]), tasks)
        result = first_node
        stack = [first_node]
        while stack:
            solution_node = stack.pop()
            current_schedule = solution_node.schedule
            remaining_tasks = solution_node.remaining_tasks
            current_schedule_real_time = solution_node.busy_time + interval_start

            search_is_finished = True
            for new_task in remaining_tasks:
                new_task_time = task_costs[processor, new_task]
                new_task_start_time = max(current_schedule_real_time, earliest_start_times[new_task])
                if new_task_start_time + new_task_time <= interval_finish:  # можно добавить таск, углубляем отбор
                    new_schedule = current_schedule.copy()
                    wait_time = new_task_start_time - current_schedule_real_time
                    if wait_time:
                        new_schedule.add_wait(processor, wait_time)
                    new_schedule.add_task(processor, new_task, new_task_time)

                    new_remaining_tasks = remaining_tasks.copy()
                    new_remaining_tasks.remove(new_task)

                    stack.append(SolutionNode(new_schedule, new_remaining_tasks))
                    search_is_finished = False

            if search_is_finished and solution_node.is_better_than(result):
                result = solution_node
        return result.schedule, result.remaining_tasks

    processors = schedule.get_processors()
    task_flow_times = schedule.task_flow_times()
    max_busy_time = schedule.max_busy_time()
    earliest_start_times = {task: _earliest_start_time(task) for task in tasks}

    remaining_tasks = tasks
    for processor in processors:
        interval_schedule, remaining_tasks = _branch_and_bound(processor, remaining_tasks)
        for new_item in interval_schedule.get_items_iter(processor):
            schedule.add_item(processor, new_item)

    return remaining_tasks


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
            if level > 0:
                # добавление тасков с уровня на свободное место в прошлый уровень
                remaining_tasks = _add_tasks_to_schedule_without_changing_busy_time(
                        result, tasks, task_costs, dependency_graph)
                if not remaining_tasks:
                    continue
            else:
                remaining_tasks = tasks

            # составление подматрицы для уровня тасок
            stage_schedule = at.get_optimal_schedule(task_costs[:, remaining_tasks],
                                                     export_intermediate_results=True,
                                                     export_file_name_prefix='level{}_'.format(level))
            # переименование тасков правильно
            for proc, items in stage_schedule:
                for item in items:
                    if isinstance(item, Task):
                        item.name = remaining_tasks[item.name]

            result.concat(stage_schedule)
    except NotDirectedAcyclicGraph:
        raise NoOptimalSchedule('Dependency graph is not a directed acyclic graph')

    return result


if __name__ == '__main__':
    import numpy as np
    import networkx as nx
    import algorithm.dependent_schedule as ads
    from input_output.visualization import draw_schedule
    from algorithm.dependent_schedule import validate_dependency_graph
    import input_output.input as i

    # task_costs = np.matrix([
    #     [9, 2, 9, 3, 10, 6, 10, 4, 10, 6],
    #     [1, 7, 8, 1, 4, 4, 8, 1, 6, 7],
    #     [9, 2, 1, 4, 4, 7, 3, 3, 5, 10]
    # ])
    task_costs = i.random_task_parameters(6, 100, 20)


    # dependency_graph = nx.DiGraph()
    # dependency_graph.add_edges_from([
    #     (0, 1),
    #     (0, 4),
    #     (0, 7),
    #     (1, 4),
    #     (1, 7),
    #     (1, 2),
    #     (1, 3),
    #     (4, 7),
    #     (4, 9),
    #     (7, 8)
    # ])
    dependency_graph = i.random_dependency_graph(list(range(0, 100)), 10, 10)

    validate_dependency_graph(dependency_graph, task_costs)

    s = ads.get_optimal_schedule(task_costs, dependency_graph)
    print(str(s))
    print('\n\n')
    draw_schedule(s, 'test_old.png')

    s = get_optimal_schedule(task_costs, dependency_graph)
    print(str(s))
    draw_schedule(s, 'test_new.png')
