import numpy as np
import networkx as nx
from itertools import dropwhile
from algorithm.graph import successive_shortest_path

def calculate_cost_matrix(task_costs):
    """
    :param np.ndarray task_costs:
    :rtype np.ndarray
    :return:
    """
    (proc_count, task_count) = task_costs.shape
    result = np.empty((proc_count * task_count, task_count), np.uint)
    for i in range(1, task_count + 1):
        submatrix_start = (i - 1) * proc_count
        result[submatrix_start: submatrix_start + proc_count] = task_costs * i
    return result


def create_timetable_graph(task_costs):
    """
    :param np.ndarray task_costs:
    :rtype nx.DiGraph
    :return:
    """
    cost_matrix = calculate_cost_matrix(task_costs)
    cost_matrix_rows, cost_matrix_cols = cost_matrix.shape

    result = nx.DiGraph()

    result.add_node('x0')
    result.add_node('y0')
    result.add_edge('y0', 'x0', capacity=cost_matrix_cols, cost=0)

    for i in range(0, cost_matrix_rows):
        new_x = 'x' + str(i + 1)
        result.add_node(new_x)
        result.add_edge('x0', new_x, capacity=1, cost=0)

        for j in range(0, cost_matrix_cols):
            new_y = 'y' + str(j + 1)
            result.add_node(new_y)
            result.add_edge(new_y, 'y0', capacity=1, cost=0)

            result.add_edge(new_x, new_y, capacity=1, cost=int(cost_matrix[i][j]))

    return result


def get_optimal_timetable(task_costs):
    """
    :param np.matrix task_costs:
    :return:
    """

    def _edge_to_task_processor_position(start_node, finish_node):
        """
        :rtype (int, int, int)
        :return:
        """
        task = int(finish_node[1:]) - 1
        recommendation = int(start_node[1:]) - 1
        position_from_end, processor = divmod(recommendation, processor_count)
        position = task_count - position_from_end - 1
        return task, processor, position

    processor_count, task_count = task_costs.shape

    problem_graph = create_timetable_graph(task_costs)
    flow_dict = successive_shortest_path(problem_graph, 'x0', 'y0')

    result = [[-1] * task_count for _ in range(0, processor_count)]
    for start_node in flow_dict:
        if start_node[0] != 'x' or start_node == 'x0':
            continue
        finish_node_dict = flow_dict[start_node]
        for finish_node in finish_node_dict:
            if finish_node_dict[finish_node] > 0:
                task, processor, position = _edge_to_task_processor_position(
                        start_node, finish_node)
                result[processor][position] = task
    return [list(dropwhile(lambda x: x < 0, a)) for a in result]


def calculate_mean_weighted_flow_time(timetable, task_costs):
    """
    :param list[list[int]] timetable:
    :param numpy.matrix task_costs:
    :return:
    """
    def _tasks_time(tasks, processor):
        acc = 0
        result = 0
        for task in tasks:
            acc += int(task_costs[processor, task])
            result += acc
        return result

    result = sum((
        _tasks_time(timetable[processor], processor)
        for processor in range(0, len(timetable))
    ))
    return result

if __name__ == '__main__':
    import input as i
    costs = i.read_task_parameters('test_data/book/task_parameters')
    timetable = [
        [2, 7, 4],
        [],
        [6, 3, 1, 5, 0]
    ]
    print(calculate_mean_weighted_flow_time(timetable, costs))
