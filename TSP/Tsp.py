import math
import copy

n = 4


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
    closest_dist = math.inf
    min_dist = 0
    start_node = nodes[0]
    start_node['visited'] = True
    sorted_nodes = [start_node]
    nodes.pop(0)
    n = n - 1
    while n != 0:
        closest_dist = math.inf
        closest_node = None
        for node in nodes:
            dist = calculate_dist(start_node, node)
            if dist < closest_dist:
                closest_dist = dist
                closest_node = node
        n = n - 1
        min_dist = min_dist + closest_dist
        nodes.remove(closest_node)
        closest_node['visited'] = True
        sorted_nodes.append(closest_node)
        start_node = closest_node
    return sorted_nodes, min_dist


def calculate_dist(start_node, end_node):
    dist = math.sqrt((start_node['x'] - end_node['x']) ** 2 + (start_node['y'] - end_node['y']) ** 2)
    return dist


def exhaustive_search(nodes, start_node, dist, permutation_node):
    permutation_node.append(start_node)
    opt_route = []
    start_node['visited'] = True
    min_dist = math.inf
    total_distance = dist
    for node in nodes:
        if not node['visited']:
            distance = calculate_dist(start_node, node)
            total_distance = total_distance + distance
            calculated_dist, found_route = exhaustive_search(nodes, node, total_distance, permutation_node)
            if calculated_dist < min_dist:
                min_dist = calculated_dist
                opt_route = found_route
            node['visited'] = False
            permutation_node.remove(node)
            total_distance = total_distance - distance
    if min_dist == math.inf:
        return total_distance, permutation_node[:]
    return min_dist, opt_route


def main():
    nodes = get_input()
    # nodes = [{'visited': False, 'x': 3, 'y': 4}, {'visited': False, 'x': 6, 'y': 8},
    #          {'visited': False, 'x': 50, 'y': 8}, {'visited': False, 'x': 11, 'y': 7}]
    # print(nodes)
    sorted_nodes, closet_dist = nearest_neighbor(copy.deepcopy(nodes))
    print('-----Solve With Nearest Neighbor-----')
    print(sorted_nodes)
    print(closet_dist)
    min_dist, opt_route = exhaustive_search(nodes, nodes[0], 0, [])
    print('-----Solve With Exhaustive Search-----')
    print(opt_route)
    print(min_dist)


if __name__ == '__main__':
    main()
