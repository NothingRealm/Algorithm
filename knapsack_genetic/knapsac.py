import numpy as np
import getopt, sys
import pdb
import random

verbose     = False
number      = 0
capacity    = 0
debug       = False
evaluation_counter = 0

def read_data(path):
    data = []
    with open(path) as knapsack:
        global number
        global capacity
        token       = knapsack.readline().split()
        number      = int(token[0])
        capacity    = int(token[1])
        for line in knapsack:
            token = line.split()
            data.append(token)
    return np.matrix(data, dtype=int)


def chromosome_generator(genes_num, chromosome_num):
    #chromosomes = np.random.randint(2, size=(genes_num, chromosome_num))
    chromosomes = np.zeros((genes_num, chromosome_num))
    return chromosomes


def evaluator(chromosomes, values, weights):
    fitness = chromosomes * values
    weight  = chromosomes * weights
    for i in range(len(weight)):
        if weight[i][0, 0] > capacity or weight[i][0, 0] == 0:
            fitness[i][0, 0] = 1
    sum_fit = np.sum(fitness)
    prob    = fitness / sum_fit
    return prob, weight, fitness


def roulette_wheel_selection(items, probs, n):
    rnds = np.random.random(size=n)
    inds = np.zeros(n, dtype=np.int)
    cum_sum = np.cumsum(probs)
    for i, rnd in enumerate(rnds):
        inds[i] = np.argmax(cum_sum >= rnd)
    return items[inds]


def cross_over(parent1, parent2, parameters={'prob': 0.4}):
    prob = parameters['prob']
    idx = int(len(parent1) / 2)
    gen1, gen2 = np.zeros(len(parent1)), np.zeros(len(parent1))
    rand = np.random.random()
    if rand <= prob:
        gen2[:idx] = parent2[:idx]
        gen1[:idx] = parent1[:idx]
        gen1[idx:] = parent2[idx:]
        gen2[idx:] = parent1[idx:]
    else:
        gen1[:idx] = parent2[:idx]
        gen2[:idx] = parent1[:idx]
        gen1[idx:] = parent1[idx:]
        gen2[idx:] = parent2[idx:]
    return gen1, gen2 


def mutation(chromosome, parameters={'prob': 0.05}):
    prob = parameters['prob']
    for i in range(len(chromosome)):
        rand = np.random.random()
        if rand < prob:
            chromosome[i] = np.random.randint(0, 2, 1)
    return chromosome

def generate_child(parents):
    global evaluation_counter
    children = []
    random.shuffle(parents)
    for i in range(0, len(parents) - 1, 2):
        chromosome1, chromosome2 = cross_over(parents[i], parents[i + 1])
        chromosome1 = mutation(chromosome1)
        chromosome2 = mutation(chromosome2)
        evaluation_counter += 2
        children += [chromosome1.tolist(), chromosome2.tolist()]
    return children


def population_selection(population, probs):    
    pairs = zip(probs.T.tolist()[0], population.tolist())
    s_pairs = sorted(pairs)
    tuples = zip(*s_pairs)
    probs, population = [list(t) for t in tuples]
    return np.asarray(population[10:30]), np.matrix(probs[10:30]).T


def main():
    global verbose, debug
    opts, args = getopt.getopt(sys.argv[1:], "vd")
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o == "-d":
            debug = True
    data = read_data('./knapsack_3.txt')
    if verbose:
        print('dataset is')
        print(data)
        print("================")
    population = chromosome_generator(20, number)
    if verbose:
        print('initial population is')
        print(population)
        print("================")
        input()
    probs, weight, fitness = evaluator(population,
                                       np.matrix(data[:,0]),
                                       np.matrix(data[:,1]))
    if verbose:
        print('evaluation result is')
        print(probs)
        print("================")
        input()
    weight  = 0
    fitness = 0
    for i in range(2000):
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
        population = np.asarray(population)
        probs, weight, fitness = evaluator(population,
                                           np.matrix(data[:,0]),
                                           np.matrix(data[:,1]))
        if debug:
            pdb.set_trace()
        population, probs = population_selection(population, probs)
        if verbose:
            print('new populatin is:')
            print(population)
            print("================")
            input()
        if verbose:
            print('prob is')
            print(probs)
            print("================")
            input()
    print('probs')
    print(probs)
    print('weight')
    print(weight)
    print('fitness')
    print(fitness)
    index = np.argmax(probs)
    print(fitness[index])


if __name__ == "__main__":
    main()

