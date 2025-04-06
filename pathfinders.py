import heapq as hq
from typing import Dict, Callable, Tuple
from math import sqrt

def dijkstra_algo(graph: Dict, start_node: int, end_node: int) -> Tuple:

    """
    Implements Dijkstra's algorithm to find the shortest path in a weighted graph.

    Parameters:
    graph (dict): A dictionary representing the graph where keys are nodes and values are dictionaries
                  of neighboring nodes with their edge weights.
    start_node (str): The starting node for the algorithm.
    end_node (str): The target node for which the shortest path is calculated.

    Returns:
    tuple: A tuple containing the shortest distance to the end_node and the path taken.
    """

    # Initialize the shortest distances from the starting node to all other nodes as infinity
    distances = {v: float("inf") for v in graph.keys()}
    # Example:
    #  |Dist. to starting node
    #---------
    # A| inf
    # B| inf
    # C| inf

    # Initialize the previous node dictionary to reconstruct the shortest path
    previous_nodes = {v: None for v in graph.keys()}
    # Example:
    #  |Prev. node
    #---------
    # A| None
    # B| None
    # C| None

    # Set the distance to the starting node as 0 since it is the starting point
    distances[start_node] = 0

    # Priority queue to store nodes along with their current shortest distance
    pq = []

    hq.heappush(pq, (0, start_node))  
    # Push the starting node with distance 0 into the priority queue

    while pq:  
    # Continue until the priority queue is empty
        
        # Pop the node with the smallest distance from the priority queue
        # and assign to current_distance and current node
        current_distance, current_node = hq.heappop(pq)
        # Example: when we start we remove start_node: "A"

        # If we have reached the target node, we can stop the algorithm
        if current_node == end_node:
            break

        # Skip the current item if the current distance is greater than the recorded shortest distance
        if current_distance > distances[current_node]:
            continue

        
        # Iterate through all neighbors of the current node:
        for neighbor_node, weight in graph[current_node].items():

            # Calculate the new distance to the neighbor:
            new_distance = current_distance + weight

            try:
                # If the new distance is shorter than the previously recorded distance:
                if new_distance < distances[neighbor_node]:

                    # Update the shortest distance to the neighbor:
                    distances[neighbor_node] = new_distance

                    # Update the previous node to reconstruct the path later:
                    previous_nodes[neighbor_node] = current_node

                    # Push the neighbor with the updated distance into the priority queue:
                    hq.heappush(pq, (new_distance, neighbor_node))

            except KeyError:
            # Protection against false neighbor nodes, which can occur in real-life data due to:
            # - Missing or incomplete edges in the graph representation.
            # - Nodes being referenced as neighbors but not defined in the graph structure.
            # This ensures the algorithm continues without crashing when encountering such inconsistencies.
                pass

    # Reconstruct the shortest path from the end_node to the start_node
    path = []

    reverse_current_node = end_node

    while reverse_current_node is not None:  
    # Traverse back using the previous_nodes dictionary
    # from End to start

        path.append(reverse_current_node)

        reverse_current_node = previous_nodes[reverse_current_node]
        
    path.reverse()  # Reverse the path to get it from start_node to end_node

    # Return the shortest distance to the end_node and the reconstructed path

    return path, distances[end_node]


def euclidian_dist(G_proj, beg_node_osmid: int, end_node_osmid: int) -> float:
# reversed (y, x) to be in line with google maps

    x1, y1 = G_proj.nodes[beg_node_osmid]["x"], G_proj.nodes[beg_node_osmid]["y"]
    x2, y2 = G_proj.nodes[end_node_osmid]["x"], G_proj.nodes[end_node_osmid]["y"]

    return sqrt((x2 - x1)**2 + (y2 - y1)**2)
    # returns distance in [m]


def Astar_algo(graph: Dict,
               graph_proj, 
               start_node: int, 
               end_node: int, 
               heuristic_func: Callable = euclidian_dist) -> Tuple:
    """
    Implements A* algorithm to find the shortest path in a weighted graph.

    Parameters:
    graph (dict): A dictionary representing the graph where keys are nodes and values are dictionaries
                  of neighboring nodes with their edge weights.
    graph_proj (MultiDiGraph): Projected graph needed to calculate heuristic function.
    start_node (str): The starting node for the algorithm.
    end_node (str): The target node for which the shortest path is calculated.
    heuristic_func (callable): A function that takes the graph projection and two node IDs 
                               (current, goal) and returns an estimated cost from current to goal. 
                               By default, it uses the Euclidean distance.

    Returns:
    tuple: A tuple containing the shortest distance to the end_node and the path taken.
    """

    # Initialize the shortest distances from the starting node to all other nodes as infinity
    g_scores = {v: float("inf") for v in graph.keys()}


    # f_scores: estimated total cost from start to goal through the node
    f_scores = {v: float("inf") for v in graph.keys()}
    f_scores[start_node] = heuristic_func(graph_proj, start_node, end_node)

    # Initialize the previous node dictionary to reconstruct the shortest path
    previous_nodes = {v: None for v in graph.keys()}

    # Example:
    #  |Prev. node
    #---------
    # A| None
    # B| None
    # C| None


    # Set the distance to the starting node as 0 since it is the starting point
    g_scores[start_node] = 0

    # Priority queue to store nodes along with their current shortest distance (f_score, node)
    pq = []

    hq.heappush(pq, (f_scores[start_node], start_node))
    # Push the starting node with distance 0 into the priority queue

    while pq:  
    # Continue until the priority queue is empty
        
        # Pop the node with the smallest distance from the priority queue
        # and assign to current_distance and current node
        f_score_dist, current_node = hq.heappop(pq)
        # Example: when we start we remove start_node: "A"

        # If we have reached the target node, we can stop the algorithm
        if current_node == end_node:
            break

        # Skip the current item if the current distance is greater than the recorded shortest distance
        if f_score_dist > f_scores[current_node]:
            continue
        
        # Iterate through all neighbors of the current node:
        for neighbor_node, weight in graph[current_node].items():

            # Calculate the new distance to the neighbor:
            new_g_score = g_scores[current_node] + weight

            try:
                # If the new distance is shorter than the previously recorded distance:
                if new_g_score < g_scores[neighbor_node]:

                    # Update the shortest distance to the neighbor:
                    g_scores[neighbor_node] = new_g_score

                    previous_nodes[neighbor_node] = current_node

                    # Update the previous node to reconstruct the path later:
                    f_scores[neighbor_node] = new_g_score + heuristic_func(graph_proj, neighbor_node, end_node)

                    # Push the neighbor with the updated distance into the priority queue:
                    hq.heappush(pq, (f_scores[neighbor_node], neighbor_node))

            except KeyError:
            # protection against false neighours nodes, which can happen in real life data
                pass

    # Reconstruct the shortest path from the end_node to the start_node
    path = []

    reverse_current_node = end_node

    while reverse_current_node is not None:  
    # Traverse back using the previous_nodes dictionary
    # from End to start

        path.append(reverse_current_node)

        reverse_current_node = previous_nodes[reverse_current_node]
        
    path.reverse()  # Reverse the path to get it from start_node to end_node

    # Return the shortest distance to the end_node and the reconstructed path

    return path, g_scores[end_node]


