import Data
import csv
import math
from collections import deque

cities = Data.Graph()

cities.add_vertex('A')
cities.add_vertex('B')
cities.add_vertex('C')
cities.add_vertex('D')

cities.add_edge('A','B',20)
cities.add_edge('A','C',42)
cities.add_edge('A','D',35)
cities.add_edge('B','C',30)
cities.add_edge('B','D',34)
cities.add_edge('C','D',12)

# cities.print_graph()

route = Data.OrderedSet()

route.add('B')
route.add('A')
route.add('C')
route.add('D')

# print(route.__len__())

def getRouteCost(city,route):
    routeCost = 0
    while route.__len__() > 1:
             routeCost += city.get_weight(route.pop(), route.peek())
    return routeCost




def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210

    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield Data.OrderedSet(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield Data.OrderedSet(pool[i] for i in indices[:r])
                break
        else:
            return

def generateRoutes(map,tourLength):
    return list(permutations(map.vertices, tourLength))

# print someRandomRoutes(cities)

# routes = someRandomRoutes(cities)
#
# for i in routes:
#     print getRouteCost(cities,i)


# data = {}

def populateCities(city):
    with open('ulysses16.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        next(spamreader, None)
        next(spamreader, None)
        reader = list(spamreader)
        # print spamreader

        for row in reader:
            city.add_vertex(row[0])

        for row in reader:
            # print row
            key = row[0]
            x = float(row[1])
            y = float(row[2])
            # distances = []
            for row2 in reader:
                x0 = float(row2[1])
                y0 = float(row2[2])
                distance = math.sqrt(math.pow((x0-x),2)+math.pow((y0-y),2))
                city.add_edge(key,row2[0],distance)
            # data[key] = distances

newCities = Data.Graph()

populateCities(newCities)
newRoutes = generateRoutes(newCities,4)

# shortestDistance = 1000000
# for route in newRoutes:
#     a = getRouteCost(newCities, route)
#     if a < shortestDistance and a!=0:
#          shortestDistance = a
# print cities.get_weight('1','2')

# print shortestDistance

for route in newRoutes:
       # if shortestDistance == getRouteCost(newCities,route):
        print route
        # break

