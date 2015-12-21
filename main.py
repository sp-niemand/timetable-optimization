import input
import sys
import visualization

if len(sys.argv) < 3:
    print("Wrong number of arguments")
    exit(255)
f = sys.argv[1]
result = sys.argv[2]

m = input.read_task_parameters(f)
visualization.write_matrix(m, result)