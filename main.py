import input
import algorithm.timetable as at
import visualization
import argparse
import os.path
import sys

# get and validate command line parameters

parser = argparse.ArgumentParser(description='Gets optimal timetables.')
parser.add_argument('--task-parameter-path', '-p', required=True, type=str, help='path to the task configuration file')
parser.add_argument('--task-dependency-path', '-d', type=str, help='path to the task dependency file')
args = parser.parse_args()

if not os.path.isfile(args.task_parameter_path):
    print('Wrong tasks parameter path given!')
    sys.exit(1)

if args.task_dependency_path and not os.path.isfile(args.task_dependency_path):
    print('Wrong tasks dependency path given!')
    sys.exit(1)

# main logic

task_costs = input.read_task_parameters(args.task_parameter_path)
if args.task_dependency_path:
    print('to be continued...')
else:
    timetable = at.get_optimal_timetable(task_costs)
    visualization.write_timetable(at.get_optimal_timetable(task_costs), task_costs)
