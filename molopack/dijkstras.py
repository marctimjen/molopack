import numpy as np
import math

def dijkstras_algoritme(adjacency_matrix, start_knude=0):
    n, m = adjacency_matrix.shape

    #Inittialize
    previous_vertex = ["" for i in range(n)]
    Shortest_distance_from_start = [math.inf for i in range(n)]  # Sætter længden af korteste vej, s til alle punkter til uendelig
    Shortest_distance_from_start[start_knude] = 0 # Sætter afstanden til start-punktet til 0.
    Visited = [] # [start_knude] #Visited
    Unvisited = [i for i in range(n)]# if i != start_knude]

    #Repeat
    while len(Unvisited) > 0: # Check if list is empty

        u = math.inf
        for i in range(len(Shortest_distance_from_start)):
            if i not in Visited:
                if Shortest_distance_from_start[i] < u:
                    u = Shortest_distance_from_start[i]
        u = Shortest_distance_from_start.index(u)

        """
        print("previous_vertex", previous_vertex)
        print("Shortest_distance_from_start", Shortest_distance_from_start)
        print("u", u)
        print("Unvisited", Unvisited)
        print("Visited", Visited)
        """
        # Opdatering af L
        for i in range(n):
            if adjacency_matrix[u][i] != -1:
                if adjacency_matrix[u][i] + Shortest_distance_from_start[u] <= Shortest_distance_from_start[i]:
                    Shortest_distance_from_start[i] = adjacency_matrix[u][i] + Shortest_distance_from_start[u]
                    previous_vertex[i] = u

        #Add the currect node to visited
        Visited.append(u)
        Unvisited.remove(u)
        print(Unvisited)



        # Udprint af graf
    return Shortest_distance_from_start, previous_vertex
