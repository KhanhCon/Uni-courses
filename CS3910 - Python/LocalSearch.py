import Data
import random
import lab1
import time
import threading

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

def randomSearchInitialiser(graph):
    initializer = list(graph.vertices)
    random.shuffle(initializer)
    return {'distance':lab1.getRouteCost(graph,initializer),'route':initializer}

def randomSearch(graph,time=5):
    return timeTermination(randomSearchInitialiser, graph, time)

def twoOptRandomSearch(graph):
    # initializer = random.sample(graph.vertices,len(graph.vertices))
    initializer = list(graph.vertices)
    random.shuffle(initializer)
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

def twoOptGreedySearch(graph):
    return lab1.findBestRoute(graph,twoOpt(greedyInitialier(graph)))

def f(f_stop,time=0,printInterval=2):
    # do something here ..
    # .

    if not f_stop.is_set():
        # call f() again in 60 seconds
        threading.Timer(printInterval, f, [f_stop,time+printInterval,printInterval]).start()
        print time

def timeTermination(function,graph, seconds=10):
    shortestDistance = 10000
    shortestRoute = None
    timeout = time.time() + seconds
    f_stop = threading.Event()
    f(f_stop)
    while time.time()<timeout:
        result = function(graph)
        if shortestDistance>result["distance"]:
            shortestDistance = result["distance"]
            shortestRoute = result["route"]
    f_stop.set()
    return {'route': shortestRoute, 'distance': shortestDistance}


print twoOptRandomSearch(lab1.newCities)
print twoOptGreedySearch(lab1.newCities)

print randomSearch(lab1.newCities)
# print timeTermination(randomSearchInitialiser(), lab1.newCities, 5)
# print random.shuffle(list(lab1.newCities.vertices))
# print lab1.newCities.vertices