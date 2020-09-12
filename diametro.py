#!/usr/bin/env pypy
from collections import defaultdict
from collections import deque
import time
import math
import sys

INF = 999999
diameter = 0
first = -1
second = -1

class Graph:  # Using a list of adjacency to represent the graph
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, source, dest, weight):
        # Storing the weights with a dict. The key is a -> b. Value is the weight himself
        self.edges[source].append(dest)
        self.edges[dest].append(source)
        self.weights[(source, dest)] = weight
        self.weights[(dest, source)] = weight

    def print_graph(self):
        # Function just to see if the algorithm is creating the right graph
        for i in range(1, self.vertices + 1):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            for vertex in self.edges[i]:
                print(" -> {}".format(vertex), end="")
            print(" \n")

    def shortest_path(self, source):
        global diameter, first, second

        visited = ["dummy"]
        distances = ["dummy"]
        stack = deque()

        for i in range(1, self.vertices + 1):
            visited.append(False)
            distances.append(INF)

        distances[source] = 0
        visited[source] = True
        stack.append(source)

        while stack:
            node = stack.popleft()
            visited[node] = False
            neighbours = self.edges[node]
            for v in neighbours:
                weight = self.weights[(node, v)]
                if distances[v] > distances[node] + weight:
                    distances[v] = distances[node] + weight
                    if not visited[v]:
                        stack.append(v)
                        visited[v] = True
        # vertices_diameter[source] = distances
        
        distances.pop(0)
        current_diameter = max(distances)
        if current_diameter > diameter:
            diameter = current_diameter
            first = source
            second = distances.index(diameter) + 1

    def dijkstra(self, source, dest):
        path_min = {source: (None, 0)}
        u = source
        visited = ["dummy"]

        for i in range(1, self.vertices + 1):
            visited.append(False)

        while u != dest:
            visited[u] = True
            destinations = self.edges[u]
            sum_weights = path_min[u][1]

            for v in destinations:
                weight = self.weights[(u, v)] + sum_weights
                if v not in path_min:
                    path_min[v] = (u, weight)
                else:
                    current_weight_v = path_min[v][1]
                    if current_weight_v > weight:
                        path_min[v] = (u, weight)
            next_dest = {w: path_min[w] for w in path_min if not visited[w]}
            u = min(next_dest, key=lambda k: next_dest[k][1])

        min_path = []
        while u is not None:
            min_path.append(u)
            next_node = path_min[u][0]
            u = next_node
        path_dist = (min_path[::-1])

        return path_dist


def read_file():
    data = []
    with open(sys.argv[1], "r") as archive: # sys.argv[1]
        lines = archive.readlines()
        for line in lines:
            data.append(line)
    infos = data[0].split(" ")
    graph = Graph(int(infos[0]))
    for i in range(1, int(infos[1]) + 1):
        edges = data[i].split()
        graph.add_edge(int(edges[0]), int(edges[1]), int(edges[2]))
    # graph.print_graph()
    operations(graph)


def operations(graph):
    for v in range(1, graph.vertices + 1):
        graph.shortest_path(v)


    min_path = graph.dijkstra(first, second)

    with open(sys.argv[2], "w") as archive: # sys.argv[2]
        archive.write(str(diameter) + "\n")
        archive.write(str(first) + " " + str(second) + "\n")
        archive.write(str(len(min_path)) + "\n")
        archive.write(str(min_path) + "\n")



if __name__ == "__main__":
    read_file()
