#!/usr/bin/env pypy
from collections import defaultdict
import time
import math
from collections import deque


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

    def shortest_path(self, source, vertices_diameter):
        visited = ["dummy"]
        distances = ["dummy"]

        for i in range(1, self.vertices + 1):
            visited.append(False)
            distances.append(math.inf)
        distances[source] = 0
        stack = deque()
        stack.append(source)
        visited[source] = True

        while stack:
            node = stack.popleft()
            visited[node] = False
            adjacencys = self.edges[node]
            for v in adjacencys:
                weight = self.weights[(node, v)]
                if distances[v] > distances[node] + weight:
                    distances[v] = distances[node] + weight
                    if not visited[v]:
                        stack.append(v)
                        visited[v] = True
        vertices_diameter[source] = distances

    def dijkstra(self, source, dest):
        # Using Dijkstra to find the minimum path between the two vertices in the init - end of a diameter path
        path_min = {source: (None, 0)}
        current_node = source
        visited = set()

        while current_node != dest:
            visited.add(current_node)
            destinations = self.edges[current_node]
            current_weight = path_min[current_node][1]

            for node in destinations:
                weight = self.weights[(current_node, node)] + current_weight
                if node not in path_min:
                    path_min[node] = (current_node, weight)
                else:
                    current_shortest_weight = path_min[node][1]
                    if current_shortest_weight > weight:
                        path_min[node] = (current_node, weight)
            next_dest = {node: path_min[node] for node in path_min if node not in visited}
            current_node = min(next_dest, key=lambda k: next_dest[k][1])

        min_path = []
        while current_node is not None:
            min_path.append(current_node)
            next_node = path_min[current_node][0]
            current_node = next_node
        path_dist = {tuple(min_path[::-1]): weight}
        return path_dist


def read_file():
    data = []
    with open("tests/graph_4.dat", "r") as archive:
        lines = archive.readlines()
        for line in lines:
            data.append(line)
    create_graph(data)


def create_graph(data):
    infos = data[0].split(" ")
    graph = Graph(int(infos[0]))
    for i in range(1, int(infos[1]) + 1):
        edges = data[i].split()
        graph.add_edge(int(edges[0]), int(edges[1]), int(edges[2]))
    # graph.print_graph()
    operations(graph)


def operations(graph):
    vertices_diameter = {}
    for v in range(1, graph.vertices + 1):
        graph.shortest_path(v, vertices_diameter)

    current_diameter = 0

    for key, distances in vertices_diameter.items():
        distances.pop(0)
        diameter = max(distances)
        if diameter > current_diameter:
            first_vertex = key
            second_vertex = (distances.index(max(distances)) + 1)
            current_diameter = diameter

    min_path = graph.dijkstra(first_vertex, second_vertex)
    for vertices in min_path.keys():
        quantity_vertices = len(vertices)

    with open("tests/output_graph_4.dat", "w") as archive:
        archive.write(str(current_diameter) + "\n")
        archive.write(str(first_vertex) + " " + str(second_vertex) + "\n")
        archive.write(str(quantity_vertices) + "\n")
        archive.write(str(list(min_path.keys())) + "\n")


def main():
    read_file()


if __name__ == "__main__":
    # start = time.time()
    main()
    # print(format((time.time() - start), ".3E"))
