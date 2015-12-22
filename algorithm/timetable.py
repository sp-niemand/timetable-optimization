import numpy as np


def calculate_cost_matrix(task_costs):
    """
    :param np.matrix task_costs:
    :rtype np.matrix
    :return: np.matrix
    """
    (proc_count, task_count) = task_costs.shape
    result = np.empty((proc_count * task_count, task_count), np.uint)
    for i in range(1, task_count + 1):
        submatrix_start = (i - 1) * proc_count
        result[submatrix_start: submatrix_start + proc_count] = task_costs * i
    return result
