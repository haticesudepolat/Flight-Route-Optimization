import networkx as nx
from src.distance import haversine
from src.data_loader import load_airports, load_routes

def build_real_graph():
    G = nx.Graph()

    airports = load_airports("data/airports.dat")
    routes = load_routes("data/routes.dat")

    # Add nodes
    for code, (lat, lon) in airports.items():
        G.add_node(code, lat=lat, lon=lon)

    # Add edges
    for src, dst in routes:
        if src in airports and dst in airports:
            lat1, lon1 = airports[src]
            lat2, lon2 = airports[dst]

            distance = haversine(lat1, lon1, lat2, lon2)

            G.add_edge(src, dst, weight=distance)

    return G