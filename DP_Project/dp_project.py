import math

costs = [
    [8, 3, 10, 43, 15, 48, 5, 40, 20, 30, 28, 24],
    [18, 1, 35, 18, 10, 19, 18, 10, 8, 5, 8, 20],
    [40, 5, 8, 13, 21, 12, 4, 27, 25, 10, 5, 15]
]

transactions = [
    [0, 20, 15],
    [20, 0, 10],
    [15, 10, 0]
]

min_cost_table = []

for i in range(len(costs)):
    min_cost_table.append([{'cost': costs[i][0], 'where': i}])

for i in range(1, len(costs[0])):
    for j in range(len(costs)):
        min = {'cost': math.inf, 'where': -1}
        for t in range(len(costs)):
            x = min_cost_table[t][i - 1]
            hold = min_cost_table[t][i - 1]['cost'] + \
                transactions[j][t] + costs[j][i]
            if hold < min['cost']:
                min['cost'] = hold
                min['where'] = t
        min_cost_table[j].append(min)
min = {'cost': math.inf, 'where': -1}
last = -1
for i in range(len(min_cost_table)):
    if min_cost_table[i][len(min_cost_table[i]) - 1]['cost'] < min['cost']:
        min = min_cost_table[i][len(min_cost_table[i]) - 1]
        last = i
print(min['cost'])
seq = []
seq.append(last + 1)
seq.append(min['where'] + 1)
where = min['where']
for i in reversed(range(1, len(costs[0]) - 1)):
    hold = min_cost_table[where][i]
    seq.append(hold['where'] + 1)
    where = hold['where']
print(seq[::-1])
