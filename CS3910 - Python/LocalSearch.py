import Data
import random
import lab1


def swap(list, i, k):
    newList = list[:]
    newList[i:k:k-i] = list[k:i:-(k - i)]
    newList[k:i:-(k-i)] = list[i:k:k - i]
    return newList

def twoOpt(iterable):
    # a = 1 if iterable[0]<iterable[-1] else -1
    neighborHood = []
    for element in xrange(len(iterable)):
        i = element
        for k in xrange(i+1,len(iterable)):
            # if a*newRoute[0]<a*newRoute[-1]:
            yield swap(iterable, i, k)
            # neighborHood.append(newRoute)
    # return neighborHood

def randomSearch(graph):
    initializer = random.sample(graph.vertices,len(graph.vertices))
    return lab1.findBestRoute(graph,twoOpt(initializer))

def greedyInitialier(graph):
    greedyRoute = []
    # print graph.vertices
    greedyRoute.append(random.choice(list(graph.vertices)))
    while len(greedyRoute)<len(graph.vertices):
        shortetDistance = 100000
        closestNode = None
        for vertex in graph.vertices:
            if vertex not in greedyRoute:
                # if graph.get_weight(greedyRoute[-1],vertex)<shortetDistance:
                a = graph.get_weight(greedyRoute[-1],vertex)
                if a < shortetDistance:
                    shortetDistance = a
                    closestNode = vertex
        greedyRoute.append(closestNode)
    return greedyRoute

def greedySearch(graph):
    return lab1.findBestRoute(graph,twoOpt(greedyInitialier(graph)))

print randomSearch(lab1.cities)
print greedySearch(lab1.cities)

