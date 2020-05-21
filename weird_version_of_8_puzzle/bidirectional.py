import pdb
import copy
import itertools

nodes   = []
st      = []
visited = []
jeffery = None
idepth  = 0
max_i   = 0
max_j   = 0
mins    = {} 
permutations = []

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
    print('sorted')
    hold = list(itertools.permutations(sorted))
    for a in hold:
        permutations.append(list(a))
    

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return [i, x.index(v)]


def generate_childs(element):
    i, j            = index_2d(element['content'], jeffery) 
    childs          = []
    new_nodes       = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if j - 1 >= 0 and element['direction'] != 'right':
        new_nodes[i][j], new_nodes[i][j - 1] = new_nodes[i][j - 1], new_nodes[i][j] 
        childs.append({'depth': element['depth'] + 1, 'content': new_nodes, 'childs': [], 'direction': 'left', 'parent': element})
    new_nodes       = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if j + 1 < max_j and element['direction'] != 'left':
        new_nodes[i][j], new_nodes[i][j + 1] = new_nodes[i][j + 1], new_nodes[i][j] 
        childs.append({'depth': element['depth'] + 1, 'content': new_nodes, 'childs': [], 'direction': 'right', 'parent': element})
    new_nodes       = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if i - 1 >= 0 and element['direction'] != 'down':
        new_nodes[i][j], new_nodes[i - 1][j] = new_nodes[i - 1][j], new_nodes[i][j] 
        childs.append({'depth': element['depth'] + 1, 'content': new_nodes, 'childs': [], 'direction': 'up', 'parent': element})
    new_nodes       = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if i + 1 < max_i and element['direction'] != 'up':
        new_nodes[i][j], new_nodes[i + 1][j] = new_nodes[i + 1][j], new_nodes[i][j] 
        childs.append({'depth': element['depth'] + 1, 'content': new_nodes, 'childs': [], 'direction': 'down', 'parent': element})
    element['childs'] = childs


def found(element, visited):
    return element['content'] in visited

def bidirectional(element, goal):
    queue1 = []
    queue2 = []
    visited = []
    visited2 = []
    queue1.append(element)
    visited.append(element['content'])
    for a in goal:
        queue2.append(a)
        visited2.append(a['content'])
    while queue1 or queue2:
        if queue1:
            element = queue1.pop(0)
            print('here')
            print(element['content'])
            for a in visited2:
                print(a)
            if found(element, visited2):
                print(element['depth'])
                print('hehrfalksflkasdjflk')
                return True
            if not element['childs']:
                generate_childs(element)
            else:
                print('here')
                break
            for child in element['childs']:
                if child['content'] in visited:
                    continue
                visited.append(child['content'])
                queue1.append(child)
        if queue2:
            goal = queue2.pop(0)
            print('there')
            print(goal['content'])
            for a in visited:
                print(a)
            if found(goal, visited):
                print(goal['depth'])
                print('hehrfalksflkasdjflk')
                return True
            if not goal['childs']:
                generate_childs(goal)
            else:
                print('here')
                break
            for child in goal['childs']:
                if child['content'] in visited:
                    continue
                visited2.append(child['content'])
                queue2.append(child)
    return False


def main():
    global idepth
    get_input()
    element = {'depth': 0, 'content': nodes, 'childs': [], 'direction': None, 'parent': None}
    el = []
    for p in permutations:
        element2 = {'depth': 0, 'content': p, 'childs': [], 'direction': None, 'parent': None}
        el.append(element2)
    print(bidirectional(element, el))
    print('found')



if __name__ == "__main__":
    main()

