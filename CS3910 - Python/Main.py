import Graph, OrderedSet
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

