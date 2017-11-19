import Data, random, operator
from lab1 import getRouteCost, populateCities, findBestRoute
from LocalSearch import swap
import numpy

def random_solutions(graph, population_size):
    random_solution = []
    for i in range(0,population_size):
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


def cross_over(parents):
    cross_point = random.randint(1, len(parents[0])-1)

    new_route = parents[0][:]
    new_route[-cross_point:] = parents[1][-cross_point:]
    parents[1][-cross_point:] = parents[0][-cross_point:]
    parents[0][:] = new_route[:]
    # print cross_point
    # print route1
    # print route2
    return parents


def mutation(route,i,k):
    return swap(route,i,k)

def swaptest(list,list2, k):
    newList = list[:]
    newList[-k:] = list2[-k:]
    list2[-k:] = list[-k:]
    list = newList
    # newList[k:i:-(k-i)] = list[i:k:k - i]
    return list

def genetic_tsp(graph,iteration,population_size=50,mutation_rate=0.01):
    mutation_rate = mutation_rate
    population = random_solutions(graph, population_size)
    # print population
    print "running EA..."
    for i in range(0,iteration):
        # print population
        for i in xrange(0,population_size):
            prob = random.uniform(0,1)
            if prob < mutation_rate:
                index = random.randint(0,len(population)-1)
                random_list = random.sample(xrange(len(graph.vertices)-1), 2)
                random_list.sort()
                population[index] = mutation(population[index],random_list[0],random_list[1])
            else:
                parents = roullet_pick(graph,population)
                # print parents
                population.remove(parents[0])
                if parents[1] in population:
                    population.remove(parents[1])
                parents = cross_over(parents)
                population.append(parents[0])
                if parents[0] != parents[1]:
                    population.append(parents[1])




    return findBestRoute(graph,population)


# print swaptest([1,2,3,4,5],[10,20,30,40,50],2)
# print random.randint(0, 1)

TSP = Data.Graph()
populateCities(TSP,'burma14.csv')
print genetic_tsp(TSP,iteration=500,population_size=35,mutation_rate=0.1)

# print random_solutions(TSP,10)
# print roullet_pick(TSP,random_solutions(TSP,10))

# print cross_over([['8', '6', '11', '5', '7', '3', '14', '9', '12', '3', '5', '6', '11', '1'], ['4', '8', '13', '2', '10', '7', '12', '9', '1', '14', '2', '4', '13', '10']])
# a = random_solutions(TSP,10)
# for i in roullet_pick(TSP,a):
#     print i

