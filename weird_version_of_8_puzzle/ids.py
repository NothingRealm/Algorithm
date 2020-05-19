import pdb
import copy


nodes   = []
jeffery = None
idepth  = 0
max_i   = 0
max_j   = 0


def get_input():
    global idepth, max_i, max_j, jeffery
    idepth  = int(input())
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
                jeffery = {'h': '#', 'c': '#'}
                hold.append(jeffery)
                continue
            node = {'h': node[:3], 'c': node[3]}
            hold.append(node)
        nodes.append(hold)


def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return [i, x.index(v)]


def generate_childs(element):
    if element['depth'] == idepth:
        return
    i, j            = index_2d(element['content'], jeffery) 
    childs          = []
    new_nodes       = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if j - 1 >= 0 and element['direction'] != 'right':
        new_nodes[i][j], new_nodes[i][j - 1] = new_nodes[i][j - 1], new_nodes[i][j] 
        childs.append({'depth': element['depth'] + 1, 'content': new_nodes, 'childs': [], 'direction': 'left'})
    new_nodes       = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if j + 1 < max_j and element['direction'] != 'left':
        new_nodes[i][j], new_nodes[i][j + 1] = new_nodes[i][j + 1], new_nodes[i][j] 
        childs.append({'depth': element['depth'] + 1, 'content': new_nodes, 'childs': [], 'direction': 'right'})
    new_nodes       = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if i - 1 >= 0 and element['direction'] != 'down':
        new_nodes[i][j], new_nodes[i - 1][j] = new_nodes[i - 1][j], new_nodes[i][j] 
        childs.append({'depth': element['depth'] + 1, 'content': new_nodes, 'childs': [], 'direction': 'up'})
    new_nodes       = copy.deepcopy(element['content'])
    new_nodes[i][j] = jeffery
    if i + 1 < max_i and element['direction'] != 'up':
        new_nodes[i][j], new_nodes[i + 1][j] = new_nodes[i + 1][j], new_nodes[i][j] 
        childs.append({'depth': element['depth'] + 1, 'content': new_nodes, 'childs': [], 'direction': 'down'})
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
    print(content)
    return True


def ids(tree):
    stack = []
    stack.append(tree)
    while stack:
        element = stack.pop()
        if found(element):
            return True
        if not element['childs']:
            generate_childs(element)
        for child in element['childs']:
            stack.append(child)
    return False


def main():
    global idepth
    get_input()
    while not ids({'depth': 0, 'content': nodes, 'childs': [], 'direction': None}):
        idepth += 1
        print(idepth)
    print('found')



if __name__ == "__main__":
    main()

