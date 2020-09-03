#!/usr/bin/env pypy

# Using adjacency lists to represent the graph
class AdjacencyList:
    def __init__(self, value, weight):
        self.vertex = value
        self.weight = weight
        self.next = None


# Using a list of adjacency lists to represent the graph
class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = [None] * (self.vertices + 1)  # The size of the graph (or the size of the array) will be V

    def add_edge(self, source, dest, weight):
        node = AdjacencyList(dest, weight)
        node.next = self.graph[source]
        self.graph[source] = node

    def print_graph(self):
        for i in range(1, self.vertices + 1):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            temp = self.graph[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")


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

    # graph.print_graph()


def main():
    read_file()


if __name__ == "__main__":
    main()
