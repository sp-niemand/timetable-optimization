import input
import algorithm.timetable
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

# main logic

if (args.task_dependency_path):
    #
    pass
else:
    task_costs = input.read_task_parameters(args.task_parameter_path)
    timetable = algorithm.timetable.get_optimal_timetable(task_costs)
    visualization.write_timetable(algorithm.timetable.get_optimal_timetable(task_costs))