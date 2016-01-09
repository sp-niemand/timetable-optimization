"""
Функционал вывода данных (на экран либо в картинку)
"""

import numpy as np
import networkx as nx


def write_graph(graph, path):
    """
    :param nx.Graph graph:
    :param str path:
    """
    nx.write_adjlist(graph, path)


def write_dependency_graph(g):
    """
    :param networkx.DiGraph g:
    :return:
    """
    from algorithm.dependency import iterate_levels
    print(
        '\n'.join('Level {}: {}'.format(
            level, ', '.join(map(str, nodes))
        ) for level, nodes in iterate_levels(g))
    )


def write_matrix(matrix, path):
    """
    :param np.matrix matrix:
    :param str path:
    """
    with open(path, 'w') as f:
        for row in matrix:
            f.write(','.join([str(x) for x in row.tolist()]) + '\n')


def write_schedule(schedule, path=None):
    """
    :param classes.schedule.Schedule schedule:
    :param str|None path:
    :return:
    """
    message = str(schedule)
    if path:
        with open(path, 'w') as f:
            f.write(message)
    else:
        print(message)


def draw_schedule(schedule, path):
    """
    Сохраняет изображение для заданного расписания

    :param classes.schedule.Schedule schedule:
    :param str path:
    :return:
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 4)

    ax.set_xlabel('time')

    sorted_processors = sorted(schedule.get_processors())
    proc_count = len(sorted_processors)

    tick_data = [(p + 0.5, '$P_{}$'.format(p)) for p in sorted_processors]
    plt.yticks(*zip(*tick_data))
    ax.set_ylim(proc_count, 0)
    max_busy_time = schedule.max_busy_time()
    ax.set_xlim(0, max_busy_time)
    ax.xaxis.set_ticks(range(0, max_busy_time), minor=True)
    ax.grid(True, axis='x', which='both')

    for processor, task_intervals in schedule.get_task_intervals().items():
        for task_name, task_start, task_finish in task_intervals:
            plt.broken_barh([(task_start, task_finish - task_start)], (processor, 1),
                            linestyle='solid', edgecolor='black', facecolor='yellow')
            plt.text(task_start + 0.5, processor + 0.5, task_name,
                     verticalalignment='center', horizontalalignment='center')

    plt.tight_layout()
    plt.savefig(path)

if __name__ == '__main__':
    from classes.schedule import Schedule
    s = Schedule([0, 1, 2])
    s.add_task(0, 0, 3)
    s.add_wait(0, 2)
    s.add_task(0, 1, 1)
    s.add_wait(1, 3)
    s.add_task(1, 2, 1)
    s.add_task(1, 3, 10)
    s.add_wait(1, 10)
    s.add_task(1, 4, 1)
    print(str(s))
    draw_schedule(s, 'test.png')
