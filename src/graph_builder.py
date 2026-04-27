import networkx as nx
from src.distance import haversine

def build_sample_graph():
    G = nx.Graph()

    # Sample airports with coordinates
    airports = {
        "IST": (41.0082, 28.9784),
        "PAR": (48.8566, 2.3522),
        "LON": (51.5074, -0.1278)
    }

    # Add nodes
    for code, (lat, lon) in airports.items():
        G.add_node(code, lat=lat, lon=lon)

    # Add edges with distance (weight)
    connections = [
        ("IST", "PAR"),
        ("PAR", "LON")
    ]

    for a, b in connections:
        lat1, lon1 = airports[a]
        lat2, lon2 = airports[b]

        distance = haversine(lat1, lon1, lat2, lon2)

        G.add_edge(a, b, weight=distance)

    return G