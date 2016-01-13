import argparse
import os.path

import input_output.export as export
import util
import input_output.input as i
from input_output.visualization import draw_schedule
from input_output.visualization import write_schedule
from util import exit_printing_error

SCHEDULE_IMAGE_NAME = 'schedule.png'
SCHEDULE_OPTIMIZED_IMAGE_NAME = 'schedule_opt.png'

DEFAULT_TASKS_TO_GENERATE = 100
DEFAULT_PROCESSORS_TO_GENERATE = 5

MAXIMUM_TASK_TIME_TO_GENERATE = 20
TASK_DEPENDENCY_LEVELS_TO_GENERATE = 6

# get and validate command line parameters

parser = argparse.ArgumentParser(description='Gets optimal schedules.')
parser.add_argument('--task-parameter-path', '-p', type=str, help='path to the task configuration file')
parser.add_argument('--task-dependency-path', '-d', type=str, help='path to the task dependency file')
parser.add_argument('--randomize-dependency', '-z', type=bool, nargs='?', const=True, default=False)

parser.add_argument('--tasks-to-generate', '-n', type=int, default=DEFAULT_TASKS_TO_GENERATE,
                    help='number of tasks to randomly generate')
parser.add_argument('--processors-to-generate', '-m', type=int, default=DEFAULT_PROCESSORS_TO_GENERATE,
                    help='number of processors to randomly generate')

parser.add_argument('--intermediate-results', '-i', type=bool, nargs='?', const=True, default=False,
                    help='should intermediate results be exported to files')
parser.add_argument('--results-path', '-r', type=str, default='.',
                    help='path for the resulting schedule image and intermediate results to be exported to')
args = parser.parse_args()

# command line arguments sanity check
if args.task_parameter_path and not os.path.isfile(args.task_parameter_path):
    exit_printing_error('Wrong tasks parameter path given!')

if args.task_dependency_path and not os.path.isfile(args.task_dependency_path):
    exit_printing_error('Wrong tasks dependency path given!')

if not os.path.isdir(args.results_path):
    exit_printing_error('Wrong results path given!')

# main logic

export.path = args.results_path

# read or generate task parameters:
if args.task_parameter_path:
    try:
        task_costs = i.read_task_parameters(args.task_parameter_path)
    except i.InvalidTaskParameters as e:
        exit_printing_error(e)
else:
    if not args.tasks_to_generate or not args.processors_to_generate:
        exit_printing_error('Wrong tasks or processors number to generate given!')
    task_costs = i.random_task_parameters(
            args.processors_to_generate, args.tasks_to_generate, MAXIMUM_TASK_TIME_TO_GENERATE)

if args.task_dependency_path or args.randomize_dependency:
    from input_output.input import read_task_dependency_graph
    import algorithm.dependent_schedule as ads
    import algorithm.optimized_dependent_schedule as aods
    from input_output.visualization import write_dependency_graph
    print("Task dependencies given")

    # read or generate task dependencies
    if args.task_dependency_path:
        try:
            task_dependencies = read_task_dependency_graph(args.task_dependency_path)
        except i.InvalidTaskDependencies as e:
            exit_printing_error(e)
    else:
        task_count = task_costs.shape[1]
        levels_to_generate = min(TASK_DEPENDENCY_LEVELS_TO_GENERATE, task_count)
        print(task_count, levels_to_generate)
        task_dependencies = i.random_dependency_graph(
                list(range(0, task_count)),
                levels_to_generate,
                task_count // levels_to_generate)

    error = ads.validate_dependency_graph(task_dependencies, task_costs)
    if error:
        exit_printing_error("Dependency graph validation error: {}".format(error))

    write_dependency_graph(task_dependencies)
    if args.intermediate_results:
        export.export_graph(task_dependencies, 'dependency_graph')
        export.export_dependency_graph(task_dependencies, 'dependency_graph')

    try:
        t0 = util.default_timer()
        schedule = ads.get_optimal_schedule(task_costs, task_dependencies)
        dt = util.default_timer() - t0
    except ads.NoOptimalSchedule as e:
        exit_printing_error(e)
    print('\nStaged method (took {0:.3f} ms to finish):'.format(dt * 1000.))
    write_schedule(schedule)
    draw_schedule(schedule, os.path.join(args.results_path, SCHEDULE_IMAGE_NAME))

    try:
        t0 = util.default_timer()
        schedule = aods.get_optimal_schedule(task_costs, task_dependencies)
        dt = util.default_timer() - t0
    except aods.NoOptimalSchedule as e:
        exit_printing_error(e)
    print('\nStaged method with packing optimization (took {0:.3f} ms to finish):'.format(dt * 1000.))
    write_schedule(schedule)
    draw_schedule(schedule, os.path.join(args.results_path, SCHEDULE_OPTIMIZED_IMAGE_NAME))
else:
    import algorithm.schedule as asc
    print("No task dependencies")
    schedule = asc.get_optimal_schedule(task_costs)
    write_schedule(schedule)
    draw_schedule(schedule, os.path.join(args.results_path, SCHEDULE_IMAGE_NAME))
