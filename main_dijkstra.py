import osmnx as ox
from pathfinders import dijkstra_algo
from utils import create_graph_dict, list_route

def route_planner(country, city, start_co, dest_co):

    specific_city = f"{city}, {country}"
    # get graph for a given area

    print("Please wait downloading map (usually takes around 40 seconds)...")
    G = ox.graph_from_place(specific_city, network_type = "drive")
    # download routs

    # reversed (y, x) to be in line with google maps
    orig = ox.distance.nearest_nodes(G, start_co[1], start_co[0]) 
    dest = ox.distance.nearest_nodes(G, dest_co[1], dest_co[0])  

    # extract nodes and edges:
    edges = ox.graph_to_gdfs(G, nodes = True, edges = True)

    graph = create_graph_dict(edges)

    print("Finding optimal route...")
    route, dist = dijkstra_algo(graph, orig, dest)

    # Draw the route
    ox.plot_graph_routes(G, [route], route_linewidth = 4, node_size = 0)

    print(f"Distance to target: {dist/1_000:.2f}km")
  
    itinerary = list_route(G, route)

    print(itinerary)

    return None

if __name__ == "__main__": 

    # Case I: KRAKÓW:
    start_coordinates = (50.06798, 19.91234) # Informatyka AGH

    destination_coordinates = (50.07680, 20.03280)  # Ośrodek Kultury Kraków-Nowa Huta

    route_planner(country = "Polska", city = "Kraków", start_co = start_coordinates , dest_co = destination_coordinates)

    # Case II: WARSZAWA
    start_coordinates = (52.24136, 21.03236) # Pomnik Syreny nad Wisłą
 
    destination_coordinates = (52.16450, 21.08910)  # Muzeum Pałacu Króla Jana III w Wilanowie

    route_planner(country = "Polska", city = "Warszawa", start_co = start_coordinates , dest_co = destination_coordinates)