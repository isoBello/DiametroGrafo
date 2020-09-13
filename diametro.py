#!/usr/bin/env pypy
from collections import defaultdict
import heapq
from copy import deepcopy
from multiprocessing import Pool
import sys

global_graph = None


class Graph:  # Using a list of adjacency to represent the graph
    def __init__(self, vertices):
        self.vertices = set(range(1, vertices + 1))
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
        for i in range(1, len(self.vertices)):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            for vertex in self.edges[i]:
                print(" -> {}".format(vertex), end="")
            print(" \n")


def dijkstra(source):
    global global_graph
    graph_copy = global_graph

    stack = [(0, source)]
    path = {source: (None, 0)}

    nodes = deepcopy(graph_copy.vertices)
    visited = [False] * (len(nodes) + 1)
    visited[source] = True
    min_path = []

    while nodes and stack:
        current_weight, u = heapq.heappop(stack)

        while u not in nodes:
            current_weight, u = heapq.heappop(stack)

        nodes.remove(u)

        for v in graph.edges[u]:
            weight = current_weight + graph_copy.weights[u, v]

            if not visited[v] or weight < path[v][1]:
                visited[v] = True
                path[v] = (u, weight)
                heapq.heappush(stack, (weight, v))

    node = u
    min_path.append(node)
    while node != source:
        next_node = [v for k, v in path.items() if k == node][0][0]
        path.pop(node)
        node = next_node
        min_path.append(node)

    return -current_weight, min_path


if __name__ == "__main__":
    # Read file, create graph, and call Dijkstra. After this rotine, write the answer in archive

    with open(sys.argv[1], "r") as archive:
        lines = archive.readlines()
        graph = Graph(int(lines[0][:lines[0].index(" ")]))
        lines.pop(0)

        for line in lines:
            edges = line.split()
            try:
                graph.add_edge(int(edges[0]), int(edges[1]), int(edges[2]))
            except IndexError:
                break

    global_graph = graph

    # Function created just to see if the graph was created correct
    # graph.print_graph()
    pool = Pool()
    results = pool.map(dijkstra, graph.vertices)

    heapq.heapify(results)
    diameter, mpath = heapq.heappop(results)

    pool.close()

    with open(sys.argv[2], "w") as archive:
        archive.write(str(-diameter) + "\n")
        archive.write(str(mpath[0]) + " " + str(mpath[-1]) + "\n")
        archive.write(str(len(mpath)) + "\n")
        archive.write(str(mpath) + "\n")
