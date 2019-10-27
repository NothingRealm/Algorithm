def delete(node):
    if node['right']:
        node_tmp = node['right']
        while node_tmp['left']:
            node_tmp = node_tmp['left']
        node_tmp['parent']['left'] = node_tmp['right']
        node_tmp['parent'] = node['parent']
        node_tmp['left'] = node['left']
        node_tmp['right'] = node['right']
    elif node['left']:
        node_tmp = node['left']
        while node_tmp['right']:
            node_tmp = node_tmp['right']
        node_tmp['parent']['right'] = node_tmp['left']
        node_tmp['parent'] = node['parent']
        node_tmp['left'] = node['left']
        node_tmp['right'] = node['right']
    else:
        if node['parent']['right'] == node:
            node['parent']['right'] = None
        else:
            node['parent']['left'] = None
        node['parent'] = None
    return node


def insert(root_node, node):
    tmp_node = root_node
    parent = None
    while True:
        if node['space'] >= tmp_node['space']:
            parent = tmp_node
            tmp_node = tmp_node['right']
            if tmp_node is None:
                tmp_node = node
                node['parent'] = parent
                parent['right'] = tmp_node
                break
        elif node['space'] < tmp_node['space']:
            parent = tmp_node
            tmp_node = tmp_node['left']
            if tmp_node is None:
                tmp_node = node
                node['parent'] = parent
                parent['left'] = tmp_node
                break


def main():
    root_node = {'space': 1000, 'left': None, 'right': None, 'parent': None}
    metal_objects = [700, 200, 400, 600, 145, 300, 120, 400, 900, 105]
    for metal_object in metal_objects:
        node = root_node
        parent = None
        while True:
            diff = node['space'] - metal_object
            if diff > 0:
                parent = node
                node = node['left']
                if not node:
                    parent['space'] = diff
                    if parent['parent']:
                        node = delete(parent)
                        insert(root_node, node)
                    break
            elif diff == 0:
                node['space'] = diff
                if node['parent']:
                    node = delete(node)
                    insert(root_node, node)
                break
            else:
                parent = node
                node = node['right']
                if node is None:
                    node = {'space': 1000 - metal_object, 'left': None, 'right': None, 'parent': None}
                    insert(root_node, node)
                    break
    print(root_node)


if __name__ == '__main__':
    main()
