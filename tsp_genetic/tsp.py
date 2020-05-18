import numpy as np
import getopt, sys
import pdb
import random
import math
import matplotlib.pyplot as plt
import matplotlib.lines as lines


verbose  = False
debug   = False
data = []


def read_data(path):
    data = []
    with open(path) as tsp:
        for line in tsp:
            token = line.split()
            d = {'n': int(token[0]), 'x': float(token[1]), 'y': float(token[2])}
            data.append(d)
    return data



def draw(nodes):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    axes.set_title('Nearest Neighbor')
    axes.set_xlabel('X')
    axes.set_ylabel('Y')
    for i in range(len(nodes)):
        node = data[nodes[i]]
        axes.scatter(node['x'], node['y'], color='black', s=100)
    for i in range(nodes.__len__() - 1):
        node1 = data[nodes[i]]
        node2 = data[nodes[i + 1]]
        axes.add_line(
            lines.Line2D([node1['x'], node2['x']],
                         [node1['y'], node2['y']]))
        axes.text((node1['x'] + node2['x']) / 2,
                  (node1['y'] + node2['y']) / 2,
                  i + 1, fontsize=15)
    plt.show()


def rank_selection(items, probs, n):
    if n == 0:
        return np.array([])

    arg_sort = np.argsort(probs)
    sorted_items = []
    for index in arg_sort:
        sorted_items.append(items[index])
    N = len(items)
    rank = np.arange(start=1, stop=N + 1)
    prob_new = 2 * rank / (N * (N + 1))

    rnds = np.random.random(size=n)
    inds = np.zeros(n, dtype=np.int)
    cum_sum = np.cumsum(prob_new)
    for i, rnd in enumerate(rnds):
        inds[i] = np.argmax(cum_sum >= rnd)
    return np.array(sorted_items)[inds]


def chromosome_generator(genes_num, chromosome_num):
    chromosomes = []
    for i in range(chromosome_num):
        c = np.random.permutation(194).tolist()
        chromosomes.append(c)
    return chromosomes 


def evaluator(chromosome):
    global data
    distance = 0
    for i in range(len(chromosome)):
        num1        = chromosome[i]
        num2        = chromosome[(i + 1) % len(chromosome)]
        a1          = data[num1]
        a2          = data[num2]
        dx          = a1['x'] - a2['x']
        dy          = a1['y'] - a2['y']
        distance    = distance + math.sqrt(dx * dx + dy * dy)
    return distance


def roulette_wheel_selection(items, probs, n):
    rnds = np.random.random(size=n)
    inds = np.zeros(n, dtype=np.int)
    cum_sum = np.cumsum(probs)
    for i, rnd in enumerate(rnds):
        inds[i] = np.argmax(cum_sum >= rnd)
    return items[inds]

def cross_over(parent1, parent2, parameters=None):
    parent1 = parent1
    parent2 = parent2
    n = len(parent1)
    start_substr = random.randint(0, n - 2)
    end_substr = random.randint(start_substr + 1, n - 1)
    child1 = parent1.copy()
    child2 = parent2.copy()
    j = end_substr
    i = end_substr
    while j != start_substr:
        if i == 194:
            print('end', end_substr)
            print('here')
        if not parent1[i] in child2[start_substr:end_substr]:
            child2[j] = parent1[i]
            j = (j + 1) % n
        i = (i + 1) % n
        if i == 194:
            print('here')
    j = end_substr
    i = end_substr
    while j != start_substr:
        if not parent2[i] in child1[start_substr:end_substr]:
            child1[j] = parent2[i]
            j = (j + 1) % n
        i = (i + 1) % n
    return child1, child2

def mutation(chro, parameters={'prob': 0.05}):
    for i in range(len(chro)):
        if np.random.random() <= parameters['prob']:
            swap_idx = np.random.randint(0, len(chro))
            chro[i], chro[swap_idx] = chro[swap_idx], chro[i]
        return chro


def reverse_mutation(chromosome, parameters={'prob': 0.15}):
    if np.random.random() <= parameters['prob']:
        chr_length = len(chromosome)

        # Two random points is selected to change values of interval
        ind_1 = np.random.randint(chr_length - 1)
        ind_2 = np.random.randint(ind_1, chr_length)

        while ind_1 < ind_2:
            chromosome[ind_1], chromosome[ind_2] = chromosome[ind_2], chromosome[ind_1]
            ind_1 += 1
            ind_2 -= 1
    return chromosome

def q_tournament_selection(items, probs, q, n):

    if n == 0:
        return np.array([])

    else:
        items, probs = warning_data_type_check_selection_algorithms(items, probs)
        index = np.arange(len(items))
        np.random.shuffle(index)
        items = items[index]
        probs = probs[index]

        selected_items = []
        len_items = len(items)

        for i in range(n):
            indexes = np.random.choice(np.arange(len_items), q, replace=False)
            selected_items.append(items[indexes[np.argmax(probs[indexes])]])
    return np.array(selected_items)


def generate_child(parents):
    children = []
    random.shuffle(parents)
    for i in range(0, len(parents) - 1, 2):
        chromosome1, chromosome2 = cross_over(parents[i], parents[i + 1])
        chromosome1 = reverse_mutation(chromosome1)
        chromosome2 = reverse_mutation(chromosome2)
        children += [chromosome1.tolist(), chromosome2.tolist()]
    return children

def population_selection(population, probs):    
    pairs = zip(probs, population)
    s_pairs = sorted(pairs)
    tuples = zip(*s_pairs)
    probs, population = [list(t) for t in tuples]
    return np.asarray(population[10:30]), np.matrix(probs[10:30]).T

def main():
    global verbose, debug, data
    opts, args = getopt.getopt(sys.argv[1:], "vd")
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o == "-d":
            debug = True
    data = read_data('tsp_data.txt')
    if verbose:
        print('data is')
        print(data)
        print("================")
        input()
    population = chromosome_generator(194, 20)
    if verbose:
        print('chromosomes are')
        print(population)
        print("================")
        input()
    probs = []
    for chromosome in population:
        #draw(chromosome)
        prob = evaluator(chromosome)
        probs.append(prob)
        #print(prob)
    fitness = 1 / np.asarray(probs)
    sum = np.sum(fitness)
    print('sum', sum)
    probs = fitness / sum
    probs = probs.tolist()
    print(probs)
    if verbose:
        print("prob is")
        print(probs)
        print("================")
    population = np.asarray(population)
    distance = []
    for i in range(5000):
        print(i)
        parents = roulette_wheel_selection(population, probs, 10)
        if verbose:
            print('selected parents are')
            print(parents)
            print("================")
            input()
        children = generate_child(parents)
        if verbose:
            print('children are')
            print(children)
            print(len(children))
            print("================")
            input()
        population = population.tolist()
        for child in children:
            population.append(child)
        probs = []
        for chromosome in population:
            prob = evaluator(chromosome)
            probs.append(prob)
        distance = probs.copy()
        fitness = 1 / np.asarray(probs)
        sum = np.sum(fitness)
        probs = fitness / sum
        probs = probs.tolist()
        if debug:
            pdb.set_trace()
        population, probs = population_selection(population, probs)
        if verbose:
            print('new populatin is:')
            print(population)
            print("================")
            print(len(population))
            input()
        if verbose:
            print('prob is')
            print(probs)
            print("================")
            print(len(probs))
            input()
    print('min distance found is')
    print(np.min(distance))


if __name__ == "__main__":
    main()
