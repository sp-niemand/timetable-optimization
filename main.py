import input
import algorithm.timetable as at
import visualization as v
import argparse
import os.path
import sys

# get and validate command line parameters

parser = argparse.ArgumentParser(description='Gets optimal timetables.')
parser.add_argument('task_parameter_path', type=str, help='path to the task configuration file')
args = parser.parse_args()

if not os.path.isfile(args.task_parameter_path):
    print('Wrong tasks parameter path given!')
    sys.exit(1)

# main logic

task_costs = input.read_task_parameters(args.task_parameter_path)
v.write_timetable(at.get_optimal_timetable(task_costs))