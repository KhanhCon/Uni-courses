from __future__ import division
from Data import Graph
import csv,random,math,lab1

class ACO:
    def __init__(self,graph):
        self.graph = graph
        self.pheromoneTrails = Graph()
        # self.initialiseTrail(self.pheromoneTrails, 'burma14.csv')
        self.p = 0.5
        self.q = 100.0
        self.alpha = 1.0
        self.beta = 5.0

    def initialiseTrail(self, fileName):
        with open(fileName, 'rb') as csvfile:
            spamreader = csv.reader(csvfile)
            next(spamreader, None)
            next(spamreader, None)
            reader = list(spamreader)

            for row in reader:
                self.pheromoneTrails.add_vertex(row[0])

            for row in reader:
                key = row[0]
                x = float(row[1])
                y = float(row[2])
                # distances = []
                for row2 in reader:
                    if row2[0] == key:
                        distance = 0
                    else:
                        x0 = float(row2[1])
                        y0 = float(row2[2])
                        distance = 0.001
                        self.pheromoneTrails.add_edge(key, row2[0], distance)

    def pheromoneDecay(self):
        for i in self.pheromoneTrails.vertices:
            for j in self.pheromoneTrails.vertices:
                if i!=j:
                    self.pheromoneTrails.set_weight(i,j,self.pheromoneTrails.get_weight(i,j)*self.p)

    def updateRoutePheromone(self, route):
        it = iter(route)
        previous = next(it)
        L = len(route)+1
        for element in it:
            self.pheromoneTrails.set_weight(previous, element, self.pheromoneTrails.get_weight(previous, element) + self.q / L)
            previous = element
            self.pheromoneTrails.set_weight(route[0], route[-1], self.pheromoneTrails.get_weight(route[0], route[-1]) + self.q / L)

    def greedyInitialier(self):
        greedyRoute = []
        currentCity = random.choice(list(self.pheromoneTrails.vertices))
        # print trail.vertices
        greedyRoute.append(currentCity)
        # print currentCity
        while len(greedyRoute) < len(self.pheromoneTrails.vertices):
            closestCity = self.chooseNextCity(currentCity,greedyRoute,self.alpha,self.beta)
            greedyRoute.append(closestCity)
            currentCity = closestCity
        return greedyRoute

    def chooseNextCity(self,currentCity,tabuList,alpha,beta):
        nextCity = None
        # print tabuList
        array = []
        for i in tabuList:
            array.append(0)
        for j in self.graph.vertices:
            if j not in tabuList:
                # print j
                pheremone = self.pheromoneTrails.get_weight(j,currentCity)
                inverseDistance = 1/self.graph.get_weight(j,currentCity)
                array.append(math.pow(inverseDistance,beta)*math.pow(pheremone,alpha))

        for j in range(0,len(array)-1):
            array[j+1] += array[j]
        r = array[-1]
        highestProbability = 0
        for city in self.graph.vertices:
             if city not in tabuList:
                pheremone = self.pheromoneTrails.get_weight(city, currentCity)
                inverseDistance = 1/self.graph.get_weight(city, currentCity)
                x = math.pow(inverseDistance, beta) * math.pow(pheremone, alpha)
                # prob = x / float(r)
                try:
                    prob = x/float(r)
                except ZeroDivisionError:
                    print x
                    print r
                if highestProbability <= prob:
                    nextCity = city
        return nextCity

        return 0

    def run(self,iteration):
        self.initialiseTrail('burma14.csv')
        bestRoute = []
        shortestCost = 10000
        print "ACO running..."
        for i in range(iteration):
            route = self.greedyInitialier()
            routeCost = lab1.getRouteCost(self.graph,route)
            self.pheromoneDecay()
            self.updateRoutePheromone(route)
            if routeCost<shortestCost:
                bestRoute = route
                shortestCost = lab1.getRouteCost(self.graph,route)
        return {'best route':bestRoute,'cost':shortestCost}

if __name__ == '__main__':
    TSP = Graph()
    lab1.populateCities(TSP, 'burma14.csv')
    aco = ACO(TSP)
    # print aco.graph.get_weight('6','11')
    print aco.run(1000)

    # print lab1.getRouteCost(lab1.TSP, ['2', '4', '6', '8', '10', '12', '14', '1', '3', '5', '7', '9', '11', '13'])