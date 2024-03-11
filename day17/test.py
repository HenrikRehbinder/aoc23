

from dijkstar import Graph, find_path
graph = Graph()
graph.add_edge(1, 2, 110)
graph.add_edge(2, 3, 125)
graph.add_edge(3, 4, 108)
path = find_path(graph, 1, 4)