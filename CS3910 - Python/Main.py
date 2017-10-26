import Graph, OrderedSet, itertools
from collections import deque

cities = Graph.Graph()

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

route = OrderedSet.OrderedSet()

route.add('B')
route.add('A')
route.add('C')
route.add('D')

# print(route.__len__())

def getRouteCost(cities,route):
    routeCost = 0
    while route.__len__() > 1:
             routeCost += cities.get_weight(route.pop(), route.peek())
    return routeCost


# print(getRouteCost(cities,route))




# def combinations(iterable, r):
#     # combinations('ABCD', 2) --> AB AC AD BC BD CD
#     # combinations(range(4), 3) --> 012 013 023 123
#     pool = tuple(iterable)
#     n = len(pool)
#     if r > n:
#         return
#     indices = list(range(r))
#     yield OrderedSet.OrderedSet(pool[i] for i in indices)
#     while True:
#         for i in reversed(range(r)):
#             if indices[i] != i + n - r:
#                 break
#         else:
#             return
#         indices[i] += 1
#         for j in range(i+1, r):
#             indices[j] = indices[j-1] + 1
#         yield OrderedSet.OrderedSet(pool[i] for i in indices)

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
    yield OrderedSet.OrderedSet(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield OrderedSet.OrderedSet(pool[i] for i in indices[:r])
                break
        else:
            return

def someRandomRoutes(cities):
    return list(permutations(cities.vertices, 4))

# print someRandomRoutes(cities)

routes = someRandomRoutes(cities)

for i in routes:
    print getRouteCost(cities,i)

