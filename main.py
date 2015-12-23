import input
import sys
import algorithm.timetable as at

if len(sys.argv) < 3:
    print("Wrong number of arguments")
    exit(255)
f = sys.argv[1]
result = sys.argv[2]

task_costs = input.read_task_parameters(f)
print(at.get_optimal_timetable(task_costs))
