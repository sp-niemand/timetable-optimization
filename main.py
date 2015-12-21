import input
import sys
import visualization

if len(sys.argv) < 3:
    print("Wrong number of arguments")
    exit(255)
dependency_graph_path = sys.argv[1]
result_path = sys.argv[2]

g = input.read_task_dependency_graph(dependency_graph_path)
visualization.write_adjlist(g, result_path)
