######## Inputs ###############

# left = ['S', 'A', 'B']
# right = [['ABacb', 'ABa', 'b'], ['aA', 'b'], ['bB', 'b']]

# left = ['S']
# right = [['aSb', 'Sab', 'ab']]

# left = ['S', 'A']
# right = [['aSaaA', 'A'], ['abA', 'bb']]

# left = ['S', 'A', 'B', 'C', 'D']
# right = [['a', 'aA', 'B', 'C'], ['aB', 'a'], ['Aa'], ['cCD', 'c'], ['ddd']]

# left = ['S', 'T', 'U', 'X']
# right = [['TaXU', 'aXU', 'TaX', 'aX'], ['UU', 'U', 'abc'], ['bSc'], ['bT', 'Tc', 'b', 'c']]

left = ['S', 'A', 'B', 'X', 'Y', 'V']
right = [['AS', 'ASB', 'SB'], ['XAS', 'XS', 'a'], ['SYS', 'VV', 'XAS', 'XS', 'a'], ['a'], ['b'], ['b']]

###################################

newRight = right.copy()
num = 0


def capitalize(k, l):
    word = right[k][l]
    hold = ''
    if word.__len__() > 1:
        for i in range(word.__len__()):
            if not word[i].isupper():
                flag = False
                for r in range(right.__len__()):
                    if right[r].__len__() == 1:
                        if right[r][0] == word[i]:
                            hold += left[r] + ','
                            flag = True
                            break
                if not flag:
                    global num
                    num += 1
                    left.append('X' + str(num))
                    right.append([word[i]])
                    hold += left[left.__len__() - 1] + ','
            else:
                hold += word[i] + ','
    else:
        hold += word[0]
    right[k][l] = hold


def separate(k, l):
    word = right[k][l]
    hold = ''
    global num
    wordArray = word.split(',')
    if wordArray.__len__() > 3:
        left.append('X' + str(num))
        num += 1
        for i in range(1, wordArray.__len__() - 1):
            hold += wordArray[i] + ','
        right[k][l] = wordArray[0] + ',' + left[left.__len__() - 1]
        right.append([hold])


def removeUnit(k, l):
    word = right[k][l]
    if word.__len__() == 1 and word.isupper():
        right[k].pop(l)
        for i in range(left.__len__()):
            if left[i] == word:
                for j in range(right[i].__len__()):
                    right[k].insert(l, right[i][j])


for i in range(right.__len__()):
    for j in range(right[i].__len__()):
        removeUnit(i, j)

for i in range(right.__len__()):
    for j in range(right[i].__len__()):
        capitalize(i, j)

num += 1
print(left)
print(right)
i = 0
for r in right:
    for j in range(len(r)):
        separate(i, j)
    i += 1

for i in range(right.__len__()):
    hold = left[i] + ' -> '
    for j in range(right[i].__len__()):
        hold += right[i][j]
        if j != right[i].__len__() - 1:
            hold += ' | '
    hold = hold.replace(',', '')
    print(hold)
