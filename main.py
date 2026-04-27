from src.graph_builder import build_real_graph

G = build_real_graph()

print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())