from src.graph_builder import build_sample_graph

G = build_sample_graph()

print("Nodes:")
for node in G.nodes(data=True):
    print(node)

print("\nEdges:")
for edge in G.edges(data=True):
    print(edge)