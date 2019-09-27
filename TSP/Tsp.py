import numpy as np
import math

n = 0


def get_input():
    global n
    nodes = []
    n = int(input('Enter the number of nodes:\n'))
    for i in range(int(n)):
        raw_node = input('Enter the node\'s coordinate\n')
        coordinate = raw_node.split(" ")
        node = {'visited': False, 'x': int(coordinate[0]), 'y': int(coordinate[1])}
        nodes.append(node)
    return nodes


def nearest_neighbor(nodes):
    global n
    start_node = nodes[0]
    start_node['visited'] = True
    sorted_nodes = []
    sorted_nodes.append(start_node)
    nodes.pop(0)
    n = n - 1
    while n != 0:
        closest_dist = math.inf
        closest_node = None
        for node in nodes:
            dist = math.sqrt((start_node['x'] - node['x']) ** 2 + (start_node['y'] - node['y']) ** 2)
            if dist < closest_dist:
                closest_dist = dist
                closest_node = node
        n = n - 1
        nodes.remove(closest_node)
        closest_node['visited'] = True
        sorted_nodes.append(closest_node)
        start_node = closest_node
    return sorted_nodes



def main():
    nodes = get_input()
    # nodes = [{'visited': False, 'x': 3, 'y': 4}, {'visited': False, 'x': 6, 'y': 8},
    #          {'visited': False, 'x': 50, 'y': 8}, {'visited': False, 'x': 11, 'y': 7}]
    print(nodes)
    sorted_nodes = nearest_neighbor(nodes)
    print(sorted_nodes)


if __name__ == '__main__':
    main()
