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

print(route.__len__())

def getRouteCost(cities,route):
    routeCost = 0
    while route.__len__() > 1:
             routeCost += cities.get_weight(route.pop(), route.peek())
    return routeCost


print(getRouteCost(cities,route))

def someRandomRoutes(cities):
    return itertools.combinations(cities.vertices, 4)



def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)