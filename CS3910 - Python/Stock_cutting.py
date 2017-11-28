import random
import time
import numpy

price = {10: 100, 13: 130, 15: 150}
stock = (10, 13, 15)
piece = [3, 3, 3, 3, 3, 4, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10, 10, 10]

# [13, 13, 10, 13, 15, 15, 13, 15, 13, 15, 15, 15, 13, 10, 15, 10, 13, 10, 13, 10]
#
# 10: 3,5,8,9,10 400
# 13: 3,4,4,6,7,10,10 520
# 15: 3,3,3,6,7,7,7,8 450

# 10.4: 10,  10,  10, 7,3,  7,3,  7,3,  6,4
# 13.3: 9,3,  6,4,
# 15.3: 7,3,5, 8,7 ,8,7

PRICE = {4300: 86, 4250: 85, 4150: 83, 3950: 79, 3800: 68, 3700: 66, 3550: 64, 3500: 63}
STOCK = (4300, 4250, 4150, 3950, 3800, 3700, 3550, 3500)
# PIECE = [2350, 2350, 2250, 2250, 2250, 2250, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2100, 2100, 2100, 2100, 2100, 2100, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050,
# 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 1950,1950, 1950, 1950, 1950,  1900,1900, 1850,1850,1850,1850,1850,1850,1850,1850,1850, 1700, 1700,1700,1650,1650,1650,1650,1650,1650, 1350, 1350,1350,1350,1350,1350,1350,1350,1350,1350,1300, 1250, 1200, 1150, 1100, 1050]
PIECE = [2350, 2350, 2250, 2250, 2250, 2250, 2200, 2200, 2200, 2200, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100,
         2100, 2100, 2100, 2100, 2100, 2100, 2100, 2050, 2050, 2050, 2050, 2050, 2050, 2000, 2000, 2000, 2000, 2000,
         2000, 2000, 2000, 2000, 2000, 2000, 1950, 1950, 1950, 1950, 1950, 1950, 1900, 1900, 1900, 1900, 1900, 1900,
         1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850,
         1850, 1850, 1850, 1850, 1700, 1700, 1700, 1700, 1700, 1650, 1650, 1350, 1350, 1350, 1350, 1350, 1350, 1350,
         1350, 1350, 1300, 1300, 1300, 1250, 1250, 1250, 1250, 1250, 1250, 1200, 1200, 1200, 1200, 1200, 1200, 1200,
         1200, 1200, 1200, 1150, 1150, 1150, 1150, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1050, 1050, 1050]

# PRICE = {120: 12, 115: 11.5, 110: 11, 105: 10.5, 100: 10}
# STOCK = (120, 115, 110, 105, 100)

l = [21, 22, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
     59, 60, 61, 63, 65, 66, 67]
q = [13, 15, 7, 5, 9, 9, 3, 15, 18, 17, 4, 17, 20, 9, 4, 19, 4, 12, 15, 3, 20, 14, 15, 6, 4, 7, 5, 19, 19, 6, 3, 7, 20,
     5, 10, 17]


def random_solution_old(stock, piece):
    solution = []
    copy_piece = []
    copy_piece[:] = piece[:]
    while len(copy_piece) > 0:
        random_stock = random.choice(stock)
        solution_pieces = []
        while len(copy_piece) > 0 and random_stock - sum(solution_pieces) >= min(copy_piece):
            random_piece = random.choice(copy_piece)
            if random_stock - sum(solution_pieces) >= random_piece:
                solution_pieces.append(random_piece)
                copy_piece.remove(random_piece)
        solution.append({"length": random_stock, "solution_pieces": solution_pieces})
    return solution


def random_population_old(population_size, stock, piece):
    population = []
    for i in range(0, population_size):
        population.append(random_solution_old(stock, piece))
    return population


def solution_cost_old(solution, price):
    cost = 0
    for i in solution:
        cost += price[i["length"]]
    return cost


def random_solution(stock, piece):
    solution = [None] * len(piece)
    for i in xrange(0, len(piece)):
        solution[i] = random.choice(stock)

    return solution


def random_population(population_size, stock, piece):
    population = []
    for i in range(0, population_size):
        population.append(random_solution(stock, piece))
    return population


def uniform_crossover(parent):
    children = [[None] * len(parent[0]), [None] * len(parent[0])]
    for i in range(0, len(parent[0])):
        if random.uniform(0, 1) < 0.5:
            children[0][i] = parent[0][i]
            children[1][i] = parent[1][i]
        else:
            children[1][i] = parent[0][i]
            children[0][i] = parent[1][i]

    return children


def single_point_crossover(parent):
    cross_point = random.randint(1, len(parent[0]) - 1)
    children = [[], []]

    children[0][:] = parent[0][:]
    children[1][:] = parent[1][:]

    children[0][cross_point:] = parent[1][cross_point:]
    children[0][:cross_point] = parent[0][:cross_point]
    children[1][cross_point:] = parent[0][cross_point:]
    children[1][:cross_point] = parent[1][:cross_point]
    # print cross_point
    # print route1
    # print route2
    return children


def mutation(parent, stock):
    child = []
    child[:] = parent[:]

    random_index = random.randint(0, len(parent) - 1)

    ranl = random.sample(xrange(0, len(stock)), 2)

    if child[random_index] != stock[ranl[0]]:
        child[random_index] = stock[ranl[0]]
    else:
        child[random_index] = stock[ranl[1]]
    return child


def scramble_mutation(parent, stock):
    child = []
    child[:] = parent[:]

    random_indexes = random.sample(xrange(0, len(child) - 1), 2)

    # ranl = random.sample(xrange(0, len(STOCK)), 2)

    for i in xrange(random_indexes[0], random_indexes[1]):
        ranl = random.randint(0, len(stock) - 1)
        child[i] = stock[ranl]

    return child


def swap(list, i, k):
    newList = list[:]
    newList[i:k:k - i] = list[k:i:-(k - i)]
    newList[k:i:-(k - i)] = list[i:k:k - i]
    return newList


def twoOpt(iterable):
    # a = 1 if iterable[0]<iterable[-1] else -1
    neighborHood = []
    for element in xrange(len(iterable)):
        i = element
        for k in xrange(i + 1, len(iterable)):
            neighborHood.append(swap(iterable, i, k))
    return neighborHood


# greedy evaluate
def evaluate2(stock, piece, price, solution):
    dict = {}
    cost = 0
    for s in stock:
        dict[s] = 0
        for i in xrange(0, len(solution)):
            if solution[i] == s:
                dict[s] = dict[s] + piece[i]
    for key in dict:
        if dict[key] % key == 0:
            cost += (dict[key] / key) * price[key]
        else:
            cost += (dict[key] / key + 1) * price[key]
    return cost


def FFD(stock_size, items, price):
    bins = [[]]
    # items.sort(reverse=True)reversed(items)
    for item in items:
        fit = True
        for bin in bins:
            l = sum(bin) + item
            if l <= stock_size:
                bin.append(item)
                fit = False
                break
        if fit:
            bins.append([item])


    # return len(bins) * price[stock_size]
    return bins


def evaluate_stable_slow(stock, piece, price, solution):
    cost = 0
    for s in stock:
        items = []
        for i in xrange(0, len(solution)):
            if solution[i] == s:
                items.append(piece[i])
        cost += FFD(s, items, price)
        # cost += len(FFD(s, items, price))*price[s]

    return cost


def evaluate(stock, piece, price, solution):
    cost = 0

    items = {}
    for s in stock:
        items[s] = []
    for i in xrange(0, len(solution)):
        items[solution[i]].append(piece[i])
    for key, value in items.iteritems():
        cost += len(FFD(key, value, price)) * price[key]
    return cost


def evaluate_2(stock, piece, price, solution):
    dict = {}
    cost = 0
    for s in stock:
        dict[s] = []
        for i in xrange(0, len(solution)):
            if solution[i] == s:
                dict[s].append(piece[i])
    print dict
    for key, value in dict.iteritems():
        # print key
        if not value:
            continue
        sum_so_far = 0
        num_of_stock = 0
        small = value[0]
        length = len(value)
        # print '--' + str(key)
        for i in xrange(0, length):
            sum_so_far += value[i]
            if i == length - 1:
                num_of_stock += 1
            elif sum_so_far + value[i + 1] > key:
                # print sum_so_far
                sum_so_far = 0
                num_of_stock += 1
        print 'num STOCK: ' + str(num_of_stock)
        cost += num_of_stock * price[key]

    return cost


def tournament_selection(stock, piece, price, population):
    tournament_population_size = random.randint(10, 20)
    tournament_population = random.sample(population, tournament_population_size)

    m1, m2 = float('inf'), float('inf')
    min1, min2 = [], []
    for x in tournament_population:
        x_fitness = evaluate(stock,piece,price,x)
        if x_fitness <= m1:
            min1, min2 = x, min1
            m1, m2 = x_fitness, m1
        elif x_fitness < m2:
            min2 = x
            m2 = x_fitness

    return [min1, min2]


def roullet_pick(stock, piece, price, population):
    # max = sum(choices.values())
    # pick = random.uniform(0, max)
    # current = 0
    # for key, value in choices.items():
    #     current += value
    #     if current > pick:
    #         return key

    total = 0
    roullet_wheel = []
    for solution in population:
        fitness = evaluate(stock, piece, price, solution)
        roullet_wheel.append(total + fitness)
        total += fitness

    sum_so_far = 0
    for key in population:
        sum_so_far += evaluate(stock, piece, price, solution)
        roullet_wheel.append(sum_so_far / total)
    # print roullet_wheel
    parents = []
    random_list = numpy.random.uniform(0, 1, 2)
    # random_list = []
    # random_list.append(random.uniform(0, 1))
    # random_list.append(random.uniform(0, 1))

    # prob1 = random.uniform(0, 1)
    # prob2 = random.uniform(0, 1)

    prob1 = random_list[0]
    prob2 = random_list[1]

    # parents = random.sample(population,2)

    for i in range(0, len(population)):
        print roullet_wheel[i]
        if prob1 < roullet_wheel[i]:
            if not population[i]:
                print "empty"
            parents.append(population[i])
            break

    for i in range(0, len(population)):
        if prob2 < roullet_wheel[i]:
            parents.append(population[i])
            break
    # print prob1
    # print prob2
    if not parents:
        print "empty parent"
    # print parents
    return parents


def print_solution(stock, piece, price, solution):
    items = {}
    for s in stock:
        items[s] = []
    for i in xrange(0, len(solution)):
        items[solution[i]].append(piece[i])
    pieces = 0
    bin_p = 0
    for key, value in items.iteritems():
        pieces += len(value)
        bins = FFD(key, value, price)
        for i in bins:
            bin_p += len(i)
        print "%i: %s" % (key, value)
        print "%i: %s" % (key, bins)

    # print bin_p
    # print pieces


def genetic_stock_cutting(stock, piece, price, iteration, population_size=50, mutation_rate=0.01):
    print "running EA_stock_cutting..."
    mutation_rate = mutation_rate
    population = random_population(population_size, stock, piece)

    # print population
    # while lowest > 3999:
    for i in range(0, iteration):
        # print population
        newGen = []

        while len(newGen) < population_size:

            prob = random.uniform(0, 1)
            if prob < mutation_rate:
                index = random.randint(0, len(population) - 1)
                newGen.append(scramble_mutation(population[index], stock))
            else:
                parents = tournament_selection(stock, piece, price, population)
                children = uniform_crossover(parents)
                newGen.append(children[0])
                if children[0] != children[1]:
                    newGen.append(children[1])
        population[:] = newGen[:]
    best = []
    lowest = 10000
    for i in population:
        cost = evaluate(stock, piece, price, i)
        if cost < lowest:
            best = i
            lowest = cost
    # print best
    print_solution(stock, piece, price, best)
    # print evaluate(STOCK, PIECE, PRICE, best)
    return lowest

if __name__ == '__main__':

    # PIECE = []
    # for i in xrange(0, len(l)):
    #     a = [l[i]] * q[i]
    #     PIECE += a

    start_time = time.time()
    # print single_point_crossover([[13,13,15,15,15,15,15,13,13,15,13,13,15,15,10,15,15,15,15,15],[10,10,13,15,15,10,10,10,10,13,13,15,15,15,13,15,10,13,15,15]])
    #
    # print evaluate([15, 13, 15, 15, 15, 15, 15, 13, 10, 13, 13, 13, 15, 15, 10, 15, 15, 15, 15, 15],price,piece,stock)
    # print evaluate_2(stock,piece,price,  [10, 10, 13, 13, 15, 10, 15, 10, 10, 10, 15, 10, 15, 13, 10, 15, 13, 10, 13, 10], )

    #
    # print mutation([15, 13, 15, 15, 15, 15, 15, 13, 10, 13, 13, 13, 15, 15, 10, 15, 15, 15, 15, 15],STOCK)

    # print FFD(10,[3, 3, 4, 5, 6, 6, 7, 8, 10, 10],price)
    print genetic_stock_cutting(stock=STOCK, piece=sorted(PIECE,reverse=True), price=PRICE, iteration=500, population_size=100,mutation_rate=0.05)

    # print genetic_stock_cutting(stock, piece, price, iteration=500, population_size=100, mutation_rate=0.2)
    # print (evaluate(stock, piece, price, [10, 10, 13, 13, 15, 10, 15, 10, 10, 10, 15, 10, 15, 13, 10, 15, 13, 10, 13, 10]))

    print("--- %s seconds ---" % (time.time() - start_time))
    # print roullet_pick(STOCK,PIECE,PRICE,[[10, 13, 13, 10, 15, 15, 13, 13, 15, 10, 15, 15, 15, 13, 15, 15, 15, 10, 15, 15], [10, 13, 13, 10, 15, 15, 13, 13, 15, 10, 15, 13, 15, 13, 15, 15, 15, 10, 15, 15], [10, 13, 13, 10, 15, 15, 13, 13, 15, 10, 15, 13, 15, 13, 15, 15, 15, 10, 15, 15], [10, 13, 13, 10, 15, 15, 13, 13, 15, 10, 15, 13, 15, 13, 15, 15, 15, 10, 15, 15]])
    # print uniform_crossover([[0,1,2,3],[4,5,6,7]])


    # pop = random_population(10,stock,piece)
    # m1, m2 = float('inf'), float('inf')
    # min1, min2 = [], []
    # for x in pop:
    #     x_fitness = evaluate(stock,piece,price,x)
    #     if x_fitness <= m1:
    #         min1, min2 = x, min1
    #         m1, m2 = x_fitness, m1
    #     elif x_fitness < m2:
    #         min2 = x
    #         m2 = x_fitness
    # print evaluate(stock,piece,price,min1)
    # print evaluate(stock,piece,price,min2)
    # print '_____'
    # l = []
    # for i in pop:
    #     l.append(evaluate(stock,piece,price,i))
    # l.sort()
    # print l