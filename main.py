import argparse
import os.path
import sys

from input_output.input import read_task_parameters
from input_output.input import InvalidTaskParameters, InvalidTaskDependencies
from input_output.visualization import write_schedule
from input_output.visualization import draw_schedule

import input_output.export as export

SCHEDULE_IMAGE_NAME = 'schedule.png'

# get and validate command line parameters

parser = argparse.ArgumentParser(description='Gets optimal schedules.')
parser.add_argument('--task-parameter-path', '-p', required=True, type=str, help='path to the task configuration file')
parser.add_argument('--task-dependency-path', '-d', type=str, help='path to the task dependency file')
parser.add_argument('--intermediate-results', '-i', type=bool, nargs='?', const=True, default=False,
                    help='should intermediate results be exported to files')
parser.add_argument('--results-path', '-r', type=str, default='.',
                    help='path for the resulting schedule image and intermediate results to be exported to')
args = parser.parse_args()

if not os.path.isfile(args.task_parameter_path):
    print('Wrong tasks parameter path given!')
    sys.exit(1)

if args.task_dependency_path and not os.path.isfile(args.task_dependency_path):
    print('Wrong tasks dependency path given!')
    sys.exit(1)

if not os.path.isdir(args.results_path):
    print('Wrong results path given!')
    sys.exit(1)

# main logic

export.path = args.results_path

try:
    task_costs = read_task_parameters(args.task_parameter_path)
except InvalidTaskParameters as e:
    print(e)
    sys.exit(1)

if args.task_dependency_path:
    from input_output.input import read_task_dependency_graph
    from algorithm.dependent_schedule import get_optimal_schedule, NoOptimalSchedule, validate_dependency_graph
    from input_output.visualization import write_dependency_graph
    print("Task dependencies given")

    try:
        task_dependencies = read_task_dependency_graph(args.task_dependency_path)
    except InvalidTaskDependencies as e:
        print(e)
        sys.exit(1)

    error = validate_dependency_graph(task_dependencies, task_costs)
    if error:
        print("Dependency graph validation error: {}".format(error))
        sys.exit(1)

    write_dependency_graph(task_dependencies)
    if args.intermediate_results:
        export.export_graph(task_dependencies, 'dependency_graph')

    try:
        schedule = get_optimal_schedule(task_costs, task_dependencies)
    except NoOptimalSchedule as e:
        print(e)
        sys.exit(1)
else:
    from algorithm.schedule import get_optimal_schedule
    print("No task dependencies")
    schedule = get_optimal_schedule(task_costs)
write_schedule(schedule)
draw_schedule(schedule, os.path.join(args.results_path, SCHEDULE_IMAGE_NAME))

# TODO: особые случаи формирования расписаний