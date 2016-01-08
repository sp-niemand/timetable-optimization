import argparse
import os.path
import sys

from input_output.input import read_task_dependency_graph, read_task_parameters
from input_output.input import InvalidTaskParameters, InvalidTaskDependencies
from input_output.visualization import write_schedule

# get and validate command line parameters

parser = argparse.ArgumentParser(description='Gets optimal schedules.')
parser.add_argument('--task-parameter-path', '-p', required=True, type=str, help='path to the task configuration file')
parser.add_argument('--task-dependency-path', '-d', type=str, help='path to the task dependency file')
parser.add_argument('--timetable-image', '-i', type=str, help='path to the resulting timetable image')
args = parser.parse_args()

if not os.path.isfile(args.task_parameter_path):
    print('Wrong tasks parameter path given!')
    sys.exit(1)

if args.task_dependency_path and not os.path.isfile(args.task_dependency_path):
    print('Wrong tasks dependency path given!')
    sys.exit(1)

if args.timetable_image and not args.timetable_image.endswith('.png'):
    print('Only *.png files can be used to visualize timetables!')
    sys.exit(1)

# main logic

try:
    task_costs = read_task_parameters(args.task_parameter_path)
except InvalidTaskParameters as e:
    print(e)
    sys.exit(1)

if args.task_dependency_path:
    from algorithm.dependent_schedule import get_optimal_schedule, NoOptimalSchedule, validate_dependency_graph
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
if args.timetable_image:
    from input_output.visualization import draw_schedule
    draw_schedule(schedule, args.timetable_image)
