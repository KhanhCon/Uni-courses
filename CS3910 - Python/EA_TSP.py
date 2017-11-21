import Data, random, operator
from lab1 import getRouteCost, populateCities, findBestRoute
from LocalSearch import swap
import numpy

def random_solutions(graph, population_size):
    random_solution = []
    for i in range(0,population_size):

        # position = i%len(graph.vertices)
        # l = list(graph.vertices)
        # route = [x for j, x in enumerate(l) if j != position]
        # random.shuffle(route)
        # route = [route[position]] + route

        route = list(graph.vertices)
        random.shuffle(route)
        random_solution.append(route)
    return random_solution

def roullet_pick(graph, solutions):

    total = 0

    for route in solutions:
        total += 1/getRouteCost(graph,route)

    roullet_wheel = []
    sum_so_far = 0
    for key in solutions:
        sum_so_far += 1/getRouteCost(graph,key)
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

    for i in range(0,len(solutions)):
        if prob1 < roullet_wheel[i]:
            parents.append(solutions[i])
            break

    for i in range(0, len(solutions)):
        if prob2 < roullet_wheel[i]:
            parents.append(solutions[i])
            break
    # print parents
    return parents

# Need fixing
def pmx_cross_over(parents):
    # cross_point = random.randint(1, len(parents[0])-1)

    def locate(original,pa2_item,parent1,parent2,crosspoint1,crosspoint2,child):

        item_index = parent2.index(pa2_item)
        pa1_same_index = parent1[item_index]
        pa2_index = parent2.index(pa1_same_index)
        if pa2_index < crosspoint2 and pa2_index >= crosspoint1:
            locate(original,parent2[pa2_index],parent1,parent2,crosspoint1,crosspoint2,child)
        else:
            child[pa2_index] = original

    cross_points = random.sample(xrange(len(parents[0])+1), 2)

    cross_points.sort()
    # print cross_points
    child1 = [None] * len(parents[0])
    child1[cross_points[0]:cross_points[1]] = parents[0][cross_points[0]:cross_points[1]]
    for i in xrange(cross_points[0],cross_points[1]):
        if parents[1][i] not in child1:
            # value_same_index = locate(i, parents[0])
            locate(parents[1][i],parents[1][i],parents[0],parents[1],cross_points[0],cross_points[1],child1)
    for i in xrange(0,len(child1)):
        if child1[i] == None:
            child1[i] = parents[1][i]

    child2 = [None] * len(parents[1])
    child2[cross_points[0]:cross_points[1]] = parents[1][cross_points[0]:cross_points[1]]
    for i in xrange(cross_points[0], cross_points[1]):
        if parents[0][i] not in child2:
            # value_same_index = locate(i, parents[0])
            locate(parents[0][i], parents[0][i], parents[1], parents[0], cross_points[0], cross_points[1], child2)
    for i in xrange(0, len(child2)):
        if child2[i] == None:
            child2[i] = parents[0][i]

    return [child1,child2]



def mutation(route,i,k):
    return swap(route,i,k)



def genetic_tsp(graph,iteration,population_size=50,mutation_rate=0.01):
    print "running EA..."
    mutation_rate = mutation_rate
    population = random_solutions(graph, population_size)
    # print population
    for i in range(0,iteration):
        # print population
        newGen = []
        while len(newGen) < population_size:
        # for i in xrange(0,population_size):
            prob = random.uniform(0,1)
            if prob < mutation_rate:
                index = random.randint(0,len(population)-1)
                random_list = random.sample(xrange(len(graph.vertices)-1), 2)
                random_list.sort()
                population[index] = mutation(population[index],random_list[0],random_list[1])
            else:
                parents = roullet_pick(graph,population)
                # print parents
                # population.remove(parents[0])
                # if parents[1] in population:
                #     population.remove(parents[1])
                children = pmx_cross_over(parents)
                newGen.append(children[0])
                if children[0] != children[1]:
                    newGen.append(children[1])
        population[:] = newGen [:]

    return findBestRoute(graph,population)


# print swaptest([1,2,3,4,5],[10,20,30,40,50],2)
# print random.randint(0, 1)
if __name__ == '__main__':
    TSP = Data.Graph()
    populateCities(TSP,'burma14.csv')
    print(genetic_tsp(TSP,iteration=1000,population_size=50,mutation_rate=0.05))

    # l = range(0,14)
    # copy = [x for j, x in enumerate(l) if j != 4]
    # print(copy)
    #
    # random.shuffle(copy)
    # copy.append(l[4])
    # print copy


# print random_solutions(TSP,10)
# print roullet_pick(TSP,random_solutions(TSP,10))

# print cross_over([['8', '6', '11', '5', '7', '3', '14', '9', '12', '3', '5', '6', '11', '1'], ['4', '8', '13', '2', '10', '7', '12', '9', '1', '14', '2', '4', '13', '10']])
# a = random_solutions(TSP,10)
# for i in roullet_pick(TSP,a):
#     print i


# [8, 4, 7, 3, 6, 2, 5, 1, 9, 0]
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#
# parents = [None,None]
# parents[0] = [8, 4, 7, 3, 6, 2, 5, 1, 9, 0]
# parents[1] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# l = [None] * 10
# print range(0,len(l)+1)
# l[0:10] = parents[0][0:10]
# print l
# print cross_over(parents)

