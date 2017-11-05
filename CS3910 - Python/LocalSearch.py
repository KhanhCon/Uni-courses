import Data
import random
import lab1


def swap(list, i, k):
    newList = list[:]
    newList[i:k:k-i] = list[k:i:-(k - i)]
    newList[k:i:-(k-i)] = list[i:k:k - i]
    return newList

mySet = [1,2,3,4,5]
reversedSet = [5,4,3,2,1]
randomSet = [2, 1, 3, 4, 5]
print mySet[-1]
newSet = mySet[:]
newSet[0:3:3] = mySet[3:0:-3]
newSet[3:0:-3] = mySet[0:3:3]
print newSet
print "==="
# print mySet[0:1]
# print mySet[1:0:-1]
# newSet = mySet[:]
# print newSet[0:1]
# newSet[0:1] = mySet[0:1:-1]
# print newSet
# print mySet[0:1]
# print mySet[1:0:-1]
# print "2"
# # print twoOptSwap(mySet,1,2)
# # print mySet[2]
# print xrange(4)

def twoOpt(iterable):
    # a = 1 if iterable[0]<iterable[-1] else -1
    neighborHood = []
    for element in xrange(len(iterable)):
        i = element
        for k in xrange(i+1,len(iterable)):
            newRoute = swap(iterable, i, k)
            # if a*newRoute[0]<a*newRoute[-1]:
            neighborHood.append(newRoute)
    return neighborHood

# for p in twoOpt(newSet):
#     print p

# twoOpt(mySet)
# print "===="
# twoOpt(reversedSet)
# print "===="
# twoOpt(randomSet)

# print random.sample(mySet,len(mySet))

def randomSearch(graph,iterable):
    initializer = random.sample(iterable,len(iterable))
    print "test**"
    print initializer
    routes = twoOpt(initializer)
    print routes
    lab1.findBestRoute(graph,routes)

print "****"

shortestDistance = 100000
shortestRoute = None
initializer = random.sample(lab1.cities.vertices,len(lab1.cities.vertices))
for route in twoOpt(initializer):
    a = lab1.getRouteCost(lab1.cities,route)
    if a < shortestDistance and a!=0:
            shortestDistance = a
            shortestRoute = route

print {'route':shortestRoute, 'distance':shortestDistance}


initializer = random.sample(lab1.cities.vertices,len(lab1.cities.vertices))
print lab1.findBestRoute(lab1.cities,initializer)


print randomSearch(lab1.cities,lab1.cities.vertices)
# print twoOpt(random.sample(lab1.cities.vertices,4))
# print lab1.getRouteCost(lab1.cities,random.sample(lab1.cities.vertices,4))