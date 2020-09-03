#!/usr/bin/env pypy
from collections import defaultdict
import sys


# Using a list of adjacency lists to represent the graph
class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = defaultdict(list)

    def add_edge(self, source, dest, weight):
        node = [dest, weight]
        self.graph[source].insert(0, node)

    def print_graph(self):
        for i in range(1, self.vertices + 1):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            temp = self.graph[i]
            for _ in enumerate(temp):
                print(" -> {}".format(temp[0][0]), end="")
            print(" \n")

    def dfs_util(self, vertex, visited, path):
        visited[vertex] = True
        path.append(vertex)
        for i in self.graph[vertex]:
            if not visited[i[0]]:
                self.dfs_util(i[0], visited, path)

    def dfs(self, vertex):
        path = []
        visited = ["dummy"]
        for i in range(1, self.vertices + 1):
            visited.append(False)
        self.dfs_util(vertex, visited, path)
        return path

    def diameter(self):
        paths = []
        for i in range(1, self.vertices + 1):
            paths.append(self.dfs(i))
        paths.sort(key=len, reverse=True)
        return paths[0]

    def dijkstra(self, path):
        source = path[0]
        dest = path[len(path) - 1]
        shortest_paths = {source: (None, 0)}
        current_node = source
        visited = set()
        destinations = []

        while current_node != dest:
            visited.add(current_node)
            for adj in self.graph[current_node]:
                destinations.append(adj[0])
                weights = {adj[0]: (current_node, adj[1])}
            weight_current = shortest_paths[current_node][1]

            for node in destinations:
                weight_node = weights.pop(node)
                weight = weight_node[1] + weight_current
                if node not in shortest_paths:
                    shortest_paths[node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[node] = (current_node, weight)
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "There's no route possible between this two vertex."
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        path = path[::-1]
        return path


def read_file():
    data = []
    with open("tests/graph_1.dat", "r") as archive:
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
    operations(graph)


def operations(graph):
    path = graph.diameter()
    diameter = len(path)
    min_path = graph.dijkstra(path)
    quantity_vertices = len(min_path)
    print(min_path)


def main():
    read_file()


if __name__ == "__main__":
    main()
