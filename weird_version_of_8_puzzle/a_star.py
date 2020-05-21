import pdb
import math
import sys
import copy
import itertools
from heapq import heappop, heappush


nodes   = []
st      = []
visited = []
jeffery = None
idepth  = 0
max_i   = 0
max_j   = 0
mins    = {} 
permutations = None

def get_input():
    global idepth, max_i, max_j, jeffery, mins, st, permutations
    max_i, max_j    = input().split()
    max_i           = int(max_i)
    max_j           = int(max_j)
    for _ in range(max_i):
        line = input()
        if line == "":
            break
        row     = line.split()
        hold    = []
        for node in row:
            if node == '#':
                jeffery = {'h': 1000, 'c': '#'}
                hold.append(jeffery)
                continue
            st.append(node[3] + node[:3])
            node = {'h': node[:3], 'c': node[3]}
            if mins.get(node['c']) == None:
                mins[node['c']] = node['h']
            else:
                if node['h'] < mins[node['c']]:
                    mins[node['c']] = node['h']
            hold.append(node)
        nodes.append(hold)
    st.sort()
    sorted = []
    flag = False
    count = 0
    le = st[0][0]
    for i in range(len(st)):
        if st[i][0] == le:
            count += 1
        else:
            le = st[i][0]
            if count != max_j:
                st.insert(i - count, jeffery)
                count = 1
                break
            count = 1
    for i in range(max_i):
        row = []
        for j in range(max_j):
            if st[max_j * i + j] == jeffery:
                row.append(jeffery)
                continue
            row.append({'h': st[max_j * i + j][1:4], 'c': st[max_j * i + j][0]})
        sorted.append(row)
    print(sorted)
    permutations = [sorted]
    permutations = list(itertools.permutations(sorted))


def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return [i, x.index(v)]


def generate_childs(element):
    #print(element['depth'])
    #for row in element['content']:
    #    print(row)
    #input()
    i, j            = index_2d(element['content'], jeffery) 
    childs          = []
    new_nodes       = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if j - 1 >= 0 and element['direction'] != 'right':
        new_nodes[i][j], new_nodes[i][j - 1] = new_nodes[i][j - 1], new_nodes[i][j] 
        childs.append(
            {'depth': element['depth'] + 1, 'content': new_nodes, 'childs': [], 'direction': 'left', 'parent': element})
    new_nodes = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if j + 1 < max_j and element['direction'] != 'left':
        new_nodes[i][j], new_nodes[i][j + 1] = new_nodes[i][j + 1], new_nodes[i][j] 
        childs.append(
            {'depth': element['depth'] + 1, 'content': new_nodes,'childs': [], 'direction': 'right', 'parent': element})
    new_nodes = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if i - 1 >= 0 and element['direction'] != 'down':
        new_nodes[i][j], new_nodes[i - 1][j] = new_nodes[i - 1][j], new_nodes[i][j] 
        childs.append(
            {'depth': element['depth'] + 1, 'content': new_nodes, 'childs': [], 'direction': 'up', 'parent': element})
    new_nodes = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if i + 1 < max_i and element['direction'] != 'up':
        new_nodes[i][j], new_nodes[i + 1][j] = new_nodes[i + 1][j], new_nodes[i][j] 
        childs.append(
            {'depth': element['depth'] + 1, 'content': new_nodes, 'childs': [], 'direction': 'down', 'parent': element})
    element['childs'] = childs


def found(element):
    content = element['content']
    i,j     = index_2d(content, jeffery)
    if j != 0:
        return False
    for i in range(max_i):
        for j in range(max_j):
            if j == max_j - 1:
                break
            a1 = content[i][j]
            if a1 == jeffery:
                continue
            a2 = content[i][j+1]
            if not a1['h'] < a2['h'] or not a1['c'] == a2['c']:
                return False
    print('depth is {}'.format(element['depth']))
    pattern = []
    x = element
    while True:
        if x['parent'] == None: 
            break
        pattern.insert(0, x['direction'])
        x = x['parent']
    print(pattern)
    for row in content:
        print(row)
    return True


def a_star(element):
    #pdb.set_trace()
    heap = []
    heap.append(element)
    visited.append(element[1]['content'])
    while heap:
        element = heap.pop(0)
        print(element[0])
        if found(element[1]):
            return True
        if not element[1]['childs']:
            generate_childs(element[1])
        for child in element[1]['childs']:
            if child['content'] in visited:
                continue
            visited.append(child['content'])
            e = (calculate_h(child['content']) + element[1]['depth'], child)
            if not heap:
                heap.append(e)
            for i in range(len(heap)):
                if i == len(heap) - 1 and e[0] > heap[i][0]:
                    heap.append(e)
                    break
                if e[0] <= heap[i][0]:
                    heap.insert(i, e)
                    break


def calculate_h(nodes):
    min_sum = sys.maxsize
    for per in permutations:
        sum = 0
        for i in range(max_i):
            for j in range(max_j):
                i_n, j_n = index_2d(per, nodes[i][j])
                sum += abs(i - i_n)  + abs(j - j_n)
                #if i_n != i or j_n != j:
                #    sum += 1
        if sum < min_sum:
            min_sum = sum
    return min_sum


def main():
    global idepth
    get_input()
    element = {'depth': 0, 'content': nodes, 'childs': [], 'direction': None, 'parent': None}
    element = (element['depth'] + calculate_h(element['content']), element)
    print(element)
    a_star(element)
    print('found')


if __name__ == "__main__":
    main()

