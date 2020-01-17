import copy
import sys

import networkx as nx
import matplotlib.pyplot as plt

sys.setrecursionlimit(150000)

v_size = 0
e_size = 0
v = []
e = []
rocket = None
lucky = None
fixed_positions = {'A': (4, 20), 'D': (0, 18), 'H': (0, 14), 'E': (4, 17), 'I': (4, 14), 'N': (4, 11), 'T': (4, 8),
                   'X': (4, 4), 'J': (8, 18), 'O': (8, 14), 'U': (10, 8), 'Y': (10, 4), 'F': (14, 18),
                   'K': (14, 14), 'P': (14, 12), 'R': (14, 9), 'V': (14, 7), 'Z': (14, 4), 'B': (16, 20),
                   'G': (16, 16),
                   'Q': (16, 12), 'S': (16, 10), 'L': (18, 13), 'C': (20, 20), 'M': (20, 12), 'W': (20, 8),
                   '[': (20, 4), 'goal': (10, 0)}


def get_input():
    global v_size, e_size, rocket, lucky
    file = open('in.txt', 'r')
    v_e = file.readline().split(" ")
    v_size = int(v_e[0])
    e_size = int(v_e[1])
    colors = file.readline().split(" ")
    for i in range(v_size - 1):
        vertex = {'id': i + 1, 'alphabet': chr(i + 1 + 64), 'color': colors[i][0], 'rocket': False, 'lucky': False,
                  'edges': [], 'visitedR': False, 'visitedL': False}
        v.append(vertex)
    v.append(
        {'id': 28, 'alphabet': 'goal', 'color': 'goal', 'rocket': False, 'lucky': False, 'edges': [], 'visitedR': False,
         'visitedL': False})
    r_l = file.readline().split()
    rocket = v[int(r_l[0]) - 1]
    lucky = v[int(r_l[1]) - 1]
    for line in file.readlines():
        edge_info = line.split(" ")
        start = int(edge_info[0])
        stop = int(edge_info[1])
        color = edge_info[2][0]
        edge = {'start': v[start - 1], 'stop': v[stop - 1], 'color': color}
        v[start - 1]['edges'].append(edge)
        e.append(edge)


seq = []
final_seq = []


def dfs(lucky, lucky_queue, rocket, rocket_queue):
    foo = lucky['alphabet'] + rocket['alphabet']
    for s in seq:
        if s == foo:
            return False
    seq.append(foo)
    draw_graph(lucky, rocket)
    if lucky['id'] == 28 or rocket['id'] == 28:
        # print('reached')
        return True
    for edge in lucky['edges']:
        if edge['color'] == rocket['color']:
            state = lucky['visitedL']
            lucky['visitedL'] = True
            flag = dfs(edge['stop'], lucky_queue, rocket, rocket_queue)  # added
            if flag:
                final_seq.append("L " + str(edge['stop']['id']))
                return True
            lucky['visitedL'] = state
            draw_graph(lucky, rocket)
    for edge in rocket['edges']:
        if edge['color'] == lucky['color']:
            state = rocket['visitedR']
            rocket['visitedR'] = True
            flag = dfs(lucky, lucky_queue, edge['stop'], rocket_queue)
            if flag:
                final_seq.append("R " + str(edge['stop']['id']))
                return True
            rocket['visitedR'] = state
            draw_graph(lucky, rocket)
    return False


def solve(lucky, rocket):
    dfs(lucky, [], rocket, [])
    for seq in reversed(final_seq):
        print(seq)


def draw_graph(lucky, rocket):
    # plt.figure(figsize=(20, 20))
    G = nx.DiGraph()
    for ver in v:
        G.add_node(ver['alphabet'])
    for ed in e:
        G.add_edge(ed['start']['alphabet'], ed['stop']['alphabet'])
    node_color = [ver['color'] for ver in v]
    # node_label = [ver['alphabet'] for ver in v]
    edge_color = [ed['color'] for ed in e]
    node_color[-1] = 'R'
    visited = []
    node_label = []
    for ver in v:
        if ver['id'] == lucky['id']:
            node_label.append("lucky")
        elif ver['id'] == rocket['id']:
            node_label.append("rocket")
        else:
            node_label.append("")
    for ver in v:
        if ver['visitedL'] and not ver['visitedR']:
            visited.append("orange")
        elif ver['visitedR'] and not ver['visitedL']:
            visited.append("black")
        elif ver['visitedR'] and ver['visitedL']:
            visited.append("brown")
        else:
            visited.append("white")
    rocket_location = fixed_positions[rocket['alphabet']]
    lucky_location = fixed_positions[lucky['alphabet']]
    plt.text(rocket_location[0] + 0.5, rocket_location[1] + 0.5, 'rocket')
    plt.text(lucky_location[0] + 0.5, lucky_location[1] + 0.5, 'lucky')
    pos = nx.spring_layout(G, pos=fixed_positions, fixed=fixed_positions)
    nx.draw_networkx_nodes(G, pos, node_color=node_color, cmap=plt.get_cmap('jet'),
                           node_size=500, label=node_label, edgecolors=visited, linewidths=2)
    nx.draw_networkx_edges(G, pos, edge_color=edge_color, arrows=True)
    nx.draw_networkx_labels(G, pos)
    plt.show()


def main():
    get_input()
    solve(lucky, rocket)


if __name__ == '__main__':
    main()
