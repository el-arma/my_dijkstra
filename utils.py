import osmnx as ox
import networkx as nx

def create_graph_dict(edges):
# Create graph dict

    temp_dict = edges[1].to_dict()

    graph = {}

    for item in temp_dict['length'].items():

        if item[0][0] not in graph.keys():
            # print('first: ', item[0])
            graph[item[0][0]] = {item[0][1]: item[1]}
            # start_node_id: {target_node_id: lenght}

        else:
            graph[item[0][0]][item[0][1]] = item[1]
    
    return graph


def list_route(G, osmid_route):
    """Convert a route (list of node OSMIDs) into a human-readable itinerary."""
    itinerary = []
    
    # Iterate through the OSMID route as node pairs
    for i in range(len(osmid_route) - 1):
        u, v = osmid_route[i], osmid_route[i + 1]

        # Get edge data (some edges might have multiple entries)
        edge_data = G.get_edge_data(u, v)
        
        if edge_data:
            # Some edges store multiple paths (parallel roads), pick the first
            data = edge_data[0] if isinstance(edge_data, dict) else edge_data

            # Extract street name (if available)
            street_name = data.get("name", "Unnamed Road")

            # Handle cases where "name" is a list (some roads have multiple names)
            if isinstance(street_name, list):
                street_name = "/".join(street_name)  # Combine multiple names

            # Avoid repeating the same street name
            if not itinerary or itinerary[-1][0] != street_name:
                itinerary.append((street_name, u, v))

    # Format the itinerary
    human_readable_itinerary = []

    for i, (street, _, _) in enumerate(itinerary):
        step = f"{i+1}. Go to: **{street}**"
        human_readable_itinerary.append(step)

    return "\n".join(human_readable_itinerary)


