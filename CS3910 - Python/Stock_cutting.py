import random
import time
import numpy


price = {10:100,13:130,15:150}
stock = (10,13,15)
piece = [3,3,3,3,3,4,4,5,6,6,7,7,7,7,8,8,9,10,10,10]


price = {4300:86, 4250:85, 4150:83, 3950:79, 3800:68, 3700:66, 3550:64, 3500:63}
stock = (4300, 4250, 4150, 3950, 3800, 3700, 3550, 3500)
# piece = [2350, 2350, 2250, 2250, 2250, 2250, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2100, 2100, 2100, 2100, 2100, 2100, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050,
# 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 1950,1950, 1950, 1950, 1950,  1900,1900, 1850,1850,1850,1850,1850,1850,1850,1850,1850, 1700, 1700,1700,1650,1650,1650,1650,1650,1650, 1350, 1350,1350,1350,1350,1350,1350,1350,1350,1350,1300, 1250, 1200, 1150, 1100, 1050]
piece = [2350, 2350, 2250, 2250, 2250, 2250, 2200, 2200, 2200, 2200, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2050, 2050, 2050, 2050, 2050, 2050, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 1950, 1950, 1950, 1950, 1950, 1950, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1700, 1700, 1700, 1700, 1700, 1650, 1650, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1300, 1300, 1300, 1250, 1250, 1250, 1250, 1250, 1250, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1150, 1150, 1150, 1150, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1050, 1050, 1050]


def random_solution_old(stock, piece):
    solution = []
    copy_piece = []
    copy_piece[:] = piece[:]
    while len(copy_piece) > 0:
        random_stock = random.choice(stock)
        solution_pieces = []
        while len(copy_piece)>0 and random_stock - sum(solution_pieces) >= min(copy_piece):
            random_piece = random.choice(copy_piece)
            if random_stock - sum(solution_pieces) >= random_piece:
                solution_pieces.append(random_piece)
                copy_piece.remove(random_piece)
        solution.append({"length":random_stock,"solution_pieces":solution_pieces})
    return solution

def random_population_old(population_size, stock, piece):
    population = []
    for i in range(0,population_size):
        population.append(random_solution_old(stock, piece))
    return population

def solution_cost_old(solution, price):
    cost = 0
    for i in solution:
        cost += price[i["length"]]
    return cost

# print(solution_cost(random_solution(stock,piece),price))

# print(range(0,10))
# print(random_population(10,stock,piece))

# def random_solution(stock, piece):
#     solution = [None] * len(stock)
#     copy_piece = []
#     copy_piece[:] = piece[:]
#     while len(copy_piece) > 0:
#         random_index = random.randint(0,len(stock)-1)
#         random_stock = stock[random_index]
#         solution_pieces = []
#         while len(copy_piece) > 0 and random_stock - sum(solution_pieces) >= min(copy_piece):
#             random_piece = random.choice(copy_piece)
#             if random_stock - sum(solution_pieces) >= random_piece:
#                 solution_pieces.append(random_piece)
#                 copy_piece.remove(random_piece)
#         if solution[random_index] is not None:
#             solution[random_index] = solution[random_index] + solution_pieces
#         else:
#             solution[random_index] = solution_pieces
#         # solution.append({"length": random_stock, "solution_pieces": solution_pieces})
#     return solution


def random_solution(stock, piece):
    solution = [None] * len(piece)
    for i in xrange(0,len(piece)):
        solution[i] = random.choice(stock)

    return solution

def random_population(population_size, stock, piece):
    population = []
    for i in range(0,population_size):
        population.append(random_solution(stock, piece))
    return population

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

def mutation(parent,stock):

    child = []
    child[:]=parent[:]

    random_index = random.randint(0, len(parent) - 1)

    ranl = random.sample(xrange(0,len(stock)),2)

    if child[random_index] != stock[ranl[0]]:
        child[random_index] = stock[ranl[0]]
    else:
        child[random_index] = stock[ranl[1]]
    return child

# print random_solution_2(stock,piece)

[[8], [7, 5, 3, 6, 3, 7], [6, 7, 3, 4, 8, 3, 9, 3, 10, 4, 10, 10, 7]]
[[9, 3, 5, 3, 6, 4, 4], [3, 10, 8, 7, 6, 8], [3, 7, 3, 10, 7, 7, 10]]

[3,  3,  3,  3,  3,  4,  4,  5,  6,  6,  7,  7,  7,  7,  8,  8,  9,  10, 10, 10]
[15, 13, 15, 15, 15, 15, 15, 13, 10, 13, 13, 13, 15, 15, 10, 15, 15, 15, 15, 15]


[13,13,15,15,15,15,15,13,13,15,13,13,15,15,10,15,15,15,15,15]

[10,10,13,15,15,10,10,10,10,13,13,15,15,15,13,15,10,13,15,15]

# for i in pmx_cross_over([[13,13,15,15,15,15,15,13,13,15,13,13,15,15,10,15,15,15,15,15],[10,10,13,15,15,10,10,10,10,13,13,15,15,15,13,15,10,13,15,15]]):
#     print i
# 10: 6+8=14 2
# 13: 3+5+6+7+7=28 3
# 15: 3+3+3+3+4+4+7+7+8+9+10+10+10=81 6

# greedy evaluate
def evaluate(stock,piece,price,solution):
    dict = {}
    cost = 0
    for s in stock:
        dict[s] = 0
        for i in xrange(0,len(solution)):
            if solution[i] == s:
                dict[s] = dict[s] + piece[i]
    for key in dict:
        if dict[key]%key == 0:
            cost += (dict[key]/key)*price[key]
        else:
            cost += (dict[key]/key+1)*price[key]
    return cost


def tournament_selection(stock,piece, price, population):

    tournament_population_size = random.randint(10,20)
    tournament_population = random.sample(population,tournament_population_size)

    m1, m2 = float('inf'), float('inf')
    for x in tournament_population:

        if evaluate(stock,piece, price, x) <= m1:
            m1, m2 = x, m1
        elif evaluate(stock,piece, price, x) < m2:
            m2 = x

    return [m1,m2]


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

        fitness = evaluate(stock,piece,price,solution)
        roullet_wheel.append(total + fitness)
        total += fitness



    sum_so_far = 0
    for key in population:
        sum_so_far += evaluate(stock,piece,price,solution)
        roullet_wheel.append(sum_so_far/total)
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


def genetic_stock_cutting(stock, piece, price, iteration, population_size=50, mutation_rate=0.01):
    print "running EA..."
    mutation_rate = mutation_rate
    population = random_population(population_size,stock,piece)
    # print population
    for i in range(0,iteration):
        # print population
        newGen = []
        while len(newGen) < population_size:
        # for i in xrange(0,population_size):
            prob = random.uniform(0,1)
            if prob < mutation_rate:
                index = random.randint(0,len(population)-1)
                newGen.append(mutation(population[index],stock))
            else:
                # print population
                parents = tournament_selection(stock,piece,price,population)
                # print parents
                # population.remove(parents[0])
                # if parents[1] in population:
                #     population.remove(parents[1])
                # print parents
                children = single_point_crossover(parents)
                newGen.append(children[0])
                if children[0] != children[1]:
                    newGen.append(children[1])
        population[:] = newGen [:]

    lowest = 10000
    for i in population:
        cost = evaluate(stock,piece,price,i)
        if cost <lowest:
            lowest = cost

    return lowest


start_time = time.time()
# print single_point_crossover([[13,13,15,15,15,15,15,13,13,15,13,13,15,15,10,15,15,15,15,15],[10,10,13,15,15,10,10,10,10,13,13,15,15,15,13,15,10,13,15,15]])
#
# print evaluate([15, 13, 15, 15, 15, 15, 15, 13, 10, 13, 13, 13, 15, 15, 10, 15, 15, 15, 15, 15],price,piece,stock)
#
# print mutation([15, 13, 15, 15, 15, 15, 15, 13, 10, 13, 13, 13, 15, 15, 10, 15, 15, 15, 15, 15],stock)

print genetic_stock_cutting(stock,piece,price,iteration=2000, population_size=200, mutation_rate=0.5)

print("--- %s seconds ---" % (time.time() - start_time))
# print roullet_pick(stock,piece,price,[[10, 13, 13, 10, 15, 15, 13, 13, 15, 10, 15, 15, 15, 13, 15, 15, 15, 10, 15, 15], [10, 13, 13, 10, 15, 15, 13, 13, 15, 10, 15, 13, 15, 13, 15, 15, 15, 10, 15, 15], [10, 13, 13, 10, 15, 15, 13, 13, 15, 10, 15, 13, 15, 13, 15, 15, 15, 10, 15, 15], [10, 13, 13, 10, 15, 15, 13, 13, 15, 10, 15, 13, 15, 13, 15, 15, 15, 10, 15, 15]])
