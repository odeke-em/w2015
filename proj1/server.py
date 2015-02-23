#!/usr/bin/env python3

import math
import doctest

# Local modules
import graph_v2
from binary_heap import BinaryHeap

def retrieve_attrs(vertex_map, v_id):
    """
    >>> print(retrieve_attrs({}, 2))
    (0, 0)
    >>> print(retrieve_attrs({65: dict(id=65, lat=-54900, lon=12828)}, 65))
    (-54900, 12828)
    >>> print(retrieve_attrs({65: dict(id=65, lat=-54900, lon=12828)}, 67))
    (0, 0)
    """
    data = vertex_map.get(v_id, {})
    return data.get('lat', 0), data.get('lon', 0) 

def cost(x_lat, x_lon, y_lat, y_lon):
    return math.sqrt((x_lat - y_lat)**2 + (x_lon - y_lon)**2)

class Server:
    def __init__(self, graph):
        self.__graph = graph
        self.__vertex_map = {}

        self.__cost_map = self.create_cost_map()

    def create_cost_map(self):
        e_iter = self.__graph.edge_mappings()
        edge_map = {}
        for src, destinations in e_iter:
            for dest in destinations:
                e = (src, dest)
                edge_map[e] = self.cost_distance(e)

        return edge_map

    def cost_distance(self, e):
        """Computes and returns the straight-line distance between the two
        vertices at the endpoints of the edge e.

        Args:
            e: An indexable container where e(0) is the vertex id for the
            starting vertex of the edge, and e(1) is the vertex id for the
            ending vertex of the edge.

        Returns:
            numeric value: the distance between the two vertices.
        """
        start_id, end_id = e
        start_lat, start_lon = retrieve_attrs(self.__vertex_map, start_id)
        end_lat, end_lon     = retrieve_attrs(self.__vertex_map, end_id)

        return cost(start_lat, start_lon, end_lat, end_lon)

    def least_cost_path_internal(self, start, dest):
        cost = lambda e: self.__cost_map.get(e, float("inf"))
        return self.least_cost_path(start, dest, cost)

    def least_cost_path(self, start, dest, cost):
        """Find and return the least cost path in graph from start
        vertext to dest vertex

        Efficiency: If E is the number of edges, the run time is
            O(E log(E)).

        Args:
            graph (Graph): The digraph defining the edges between the
                vertices.
            start: The vertex where the path starts. It is assumed
                that start is a vertex of graph.
            dest: The vertex where the path ends. It is assumed
                that end is a vertex of graph.
            cost: A function, taking a single edge as a parameter and
                returning the cost of the edge. For its interface,
                see the definition of cost_distance.

        Returns:
            list: A potentially empty list (if no path can be found) of
                the vertices in the graph. If there was a path, the first
                vertex is always start, the last is always dest in the list.
                Any two consecutive vertices correspond to some edge in graph.

        >>> graph = graph_v2.Graph({1, 2, 3, 4, 5, 6}, [(1,2), (1,3), (1,6), (2,1),\
                    (2,3), (2,4), (3,1), (3,2), (3,4), (3,6), (4,2), (4,3),\
                    (4,5), (5,4), (5,6), (6,1), (6,3), (6,5)])
        >>> weights = {(1,2): 7, (1,3): 9, (1,6): 14, (2,1): 7, (2,3): 10,\
                    (2,4): 15, (3,1): 9, (3,2): 10, (3,4): 11, (3,6): 2,\
                    (4,2): 15, (4,3):11, (4,5): 6, (5,4): 6, (5,6): 9, (6,1): 14,\
                    (6,3): 2, (6,5): 9}
        >>> cost = lambda e: weights.get(e, float("inf"))
        >>> srv = Server(graph)
        >>> srv.least_cost_path(1, 5, cost)
        [1, 3, 6, 5]
        """
        if not (self.__graph.is_vertex(start) and self.__graph.is_vertex(dest)):
            return []

        if start == dest:
            return [start]

        R = {}
        dist = {}
        PQ = BinaryHeap()
        PQ.add((start, start), 0)
        while len(PQ):
            head, val = PQ.pop_min()
            prev, curr = head
            if curr not in R:
                R[curr] = prev
                dist[curr] = val
                neighbours = self.__graph.neighbours(curr)

                for nb in neighbours:
                    edge = (curr, nb)
                    PQ.add(edge, val + cost(edge))

        return back_track(R, dest)

    def closest_point(self, lat, lon):
        points = []

def back_track(connection_map, cur):
    """
    >>> print(back_track({1: 1, 2: 4, 5: 6, 9: 2}, 10))
    []
    >>> print(back_track({1: 1, 2: 4, 5: 6, 9: 2}, 9))
    [4, 2, 9]
    """

    if cur not in connection_map:
        return []

    walk = []
    found = {}

    while 1:
        if cur not in found:
            found[cur] = 1
            walk.append(cur)

        cur = connection_map.pop(cur, None)
        if cur is None:
            break

    # Reverse the walk
    return walk[::-1]

def main():
    server = Server(graph_v2.Graph({1, 2, 3, 4, 5, 6}, [(1,2), (1,3), (1,6), (2,1),\
                    (2,3), (2,4), (3,1), (3,2), (3,4), (3,6), (4,2), (4,3),\
                    (4,5), (5,4), (5,6), (6,1), (6,3), (6,5)]))
    weights = {(1,2): 7, (1,3): 9, (1,6): 14, (2,1): 7, (2,3): 10,\
                    (2,4): 15, (3,1): 9, (3,2): 10, (3,4): 11, (3,6): 2,\
                    (4,2): 15, (4,3):11, (4,5): 6, (5,4): 6, (5,6): 9, (6,1): 14,\
                    (6,3): 2, (6,5): 9}
    cost = lambda e: weights.get(e, float("inf"))
    print(server.least_cost_path(1, 5, cost))

def create_server():
    g, vmap= graph_v2.deserialize_graph()
    srv = Server(g)
    return srv, vmap

if __name__ == '__main__':
    # main()
    doctest.testmod()
