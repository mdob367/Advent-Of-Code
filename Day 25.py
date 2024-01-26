import numpy as np
import re
import math
import itertools
import get_input
from functools import lru_cache
from collections import OrderedDict
import time
import pprint
from collections import defaultdict
from collections import deque

class Graph(object):
    def __init__(self, connections):
        self._graph = defaultdict(set)
        self.connections = connections
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """
        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        self._graph[node2].add(node1)

    
    def remove_node(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.items():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def remove_connection(self, cnx):
        """ Remove connection between node1 and node2 """
        node1, node2 = cnx
        try:
            self._graph[node1].remove(node2)
            self._graph[node2].remove(node1)
        except KeyError:
            print('Invalid connection: {}'.format(cnx))
            assert False
            pass

    def add_connection(self, cnx):
        """ Remove connection between node1 and node2 """
        node1, node2 = cnx
        self.add(node1, node2)


    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    
    def find_shortest_path(self, start, end):
        """Find the shortest path between start and end nodes."""
        if start not in self._graph or end not in self._graph:
            return None

        # Check if any path exists
        if end not in self.find_reachable(start):
            return None

        # Initialize queues and visited set
        queue = deque([[start]])
        visited = set([start])

        while queue:
            # Get the first path from the queue
            path = queue.popleft()
            node = path[-1]

            # Path found
            if node == end:
                return path

            # Enumerate all adjacent nodes, construct a new path and push it into the queue
            for adjacent in self._graph.get(node, []):
                if adjacent not in visited:
                    visited.add(adjacent)
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)

        # Path not found
        return None


    def find_all_paths(self, node1, node2):
        """ Find all short paths between node1 and node2"""
        
        paths=[]
        new_path = self.find_shortest_path(node1, node2)
        while new_path:
            paths.append(new_path)
            for node in range(len(new_path)-1):
                self.remove_connection((new_path[node], new_path[node+1]))
            new_path = self.find_shortest_path(node1, node2)

        return paths
    

    def find_reachable(self, node):
        to_test = [node]
        tested = set()
        while to_test:
            curr = to_test.pop()
            tested.add(curr)
            for n in self._graph[curr]:
                if n not in tested:
                    to_test.append(n)
        return tested
    
    def count_separate(self):
        nodes = set(self._graph.keys())
        count = []
        while nodes:
            node = nodes.pop()
            reachable = self.find_reachable(node)
            count.append(len(reachable))

            nodes = nodes - reachable
        return count

    
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))


def parse_graph(graph):
    graph = graph.split('\n')
    res = []
    for line in graph:
        line = line.split(': ')
        node, children = line
        for c in children.split(' '):
            res.append((node, c))
    graph = Graph(res)
    return graph

example = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""

graph = parse_graph(get_input.get_input_file(25))
# graph = parse_graph(example)
pretty_print = pprint.PrettyPrinter()
# pretty_print.pprint(graph._graph)

# print(graph.count_separate())
# graph.remove_connection('hfx', 'pzl')
# graph.remove_connection('bvb', 'cmg')
# graph.remove_connection('nvd', 'jqt')
# print(graph.count_separate())


test_graph = Graph(graph.connections)
node_list = list(test_graph._graph.keys())
first_node = node_list[0]
print(len(graph.connections), first_node, test_graph.count_separate())

connection_count = defaultdict(int)

for node in node_list[1:]:
    print(first_node, node)
    graph_copy = graph.connections.copy()
    paths = []
    test_graph = Graph(graph_copy)
    path = test_graph.find_shortest_path(first_node, node)
    while path:
        print('path length: ', len(path))
        for i in range(len(path)-1):
            if (path[i], path[i+1]) in graph_copy:
                graph_copy.remove((path[i], path[i+1]))
            else:
                graph_copy.remove((path[i+1], path[i]))
        test_graph = Graph(graph_copy)
        paths.append(path)
        if len(paths) > 3:
            break
        path = test_graph.find_shortest_path(first_node, node)
    print(first_node, node, len(paths))
    if len(paths) <= 3 :
        for path in paths:
            for i_node in range(len(path)-1):
                # Increment the count for each node in the path
                connection_count[(path[i_node], path[i_node+1])] += 1
connection_count = OrderedDict(sorted(connection_count.items(), key=lambda t: t[1], reverse=True))

#sort node_counts
# connection_count = OrderedDict(sorted(connection_count.items(), key=lambda t: t[1], reverse=True))
# print(*connection_count.items(), sep='\n')
# print(list(connection_count.keys())[0])
print(len(test_graph.connections))
print(connection_count)
test_graph = Graph(graph.connections)
for cnx in list(connection_count.keys()):
    if len(test_graph.count_separate()) >1:
        break
    print(cnx)
    test_graph.remove_connection(cnx)
print(len(test_graph.connections))

print(test_graph.count_separate())
exit()

test_graph = Graph(graph.connections)
print(test_graph.count_separate())
for i in range(3):
    test_graph.remove_connection(list(connection_count.keys())[i])

print(test_graph)
print(test_graph.count_separate())