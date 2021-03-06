import math
import copy
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import time

n = 4


def get_input():
    f = open('input.txt', 'r')
    lines_nodes = f.readlines()
    global n
    nodes = []
    n = int(lines_nodes[0])
    lines_nodes.pop(0)
    for row in lines_nodes:
        raw_node = row
        coordinate = raw_node.split(" ")
        node = {'visited': False, 'x': int(coordinate[0]), 'y': int(coordinate[1])}
        nodes.append(node)
    return nodes


def nearest_neighbor(nodes):
    global n
    closest_dist = math.inf
    min_dist = 0
    begin = nodes[0]
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
    sorted_nodes.append(begin)
    min_dist = min_dist + calculate_dist(start_node, begin)
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
        total_distance = total_distance + calculate_dist(start_node, nodes[0])
        # print(total_distance)
        # print(permutation_node[:])
        return total_distance, permutation_node[:]
    return min_dist, opt_route


def draw(nodes_near, nodes_exhaustive):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    if nodes_near is not None:
        axes.set_title('Nearest Neighbor')
        axes.set_xlabel('X')
        axes.set_ylabel('Y')
        for node in nodes_near:
            axes.scatter(node['x'], node['y'], color='black', s=100)
        for i in range(nodes_near.__len__() - 1):
            axes.add_line(
                lines.Line2D([nodes_near[i]['x'], nodes_near[i + 1]['x']],
                             [nodes_near[i]['y'], nodes_near[i + 1]['y']]))
            axes.text((nodes_near[i]['x'] + nodes_near[i + 1]['x']) / 2,
                      (nodes_near[i]['y'] + nodes_near[i + 1]['y']) / 2,
                      i + 1, fontsize=15)
    if nodes_exhaustive is not None:
        axes.set_xlabel('X')
        axes.set_ylabel('Y')
        axes.set_title('Exhaustive Search')
        for node in nodes_exhaustive:
            axes.scatter(node['x'], node['y'], color='black', s=100)
        for i in range(nodes_exhaustive.__len__() - 1):
            axes.add_line(
                lines.Line2D([nodes_exhaustive[i]['x'], nodes_exhaustive[i + 1]['x']],
                             [nodes_exhaustive[i]['y'], nodes_exhaustive[i + 1]['y']]))
            axes.text((nodes_exhaustive[i]['x'] + nodes_exhaustive[i + 1]['x']) / 2,
                      (nodes_exhaustive[i]['y'] + nodes_exhaustive[i + 1]['y']) / 2,
                      i + 1, fontsize=15)
    plt.show()


def main():
    nodes = get_input()
    sorted_nodes = None
    opt_route = None
    # nodes = [{'visited': False, 'x': 3, 'y': 4}, {'visited': False, 'x': 6, 'y': 8},
    #          {'visited': False, 'x': 50, 'y': 8}, {'visited': False, 'x': 11, 'y': 7}]
    # print(nodes)
    # t0 = time.time()
    # sorted_nodes, closet_dist = nearest_neighbor(copy.deepcopy(nodes))
    # t1 = time.time()
    # print('-----Solve With Nearest Neighbor-----')
    # print(t1 - t0)
    # print(sorted_nodes)
    # print(closet_dist)
    # print('-------------------------------------')
    t0 = time.time()
    min_dist, opt_route = exhaustive_search(nodes, nodes[0], 0, [])
    t1 = time.time()
    print(t1 - t0)
    # print('-----Solve With Exhaustive Search-----')
    opt_route.append(nodes[0])
    print(opt_route)
    print(min_dist)
    draw(sorted_nodes, opt_route)


if __name__ == '__main__':
    main()
