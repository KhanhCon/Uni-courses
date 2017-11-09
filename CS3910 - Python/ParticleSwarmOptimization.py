import ContinuousRandomSearch
import AntennaArray
import time
import numpy

class Particle:
    # swarmSize = 20+...
    INERTIAL = 0.721
    COGNITIVE = 1.1193
    SOCIAL = 2.0
    def __init__(self,velocity,position):
        self.velocity = velocity
        self.position = position
        self.bestPosition = position
    def update(self,antennaArray,globalBest):
        # r1 = numpy.random.uniform(0.0, 1.0)
        # r2 = numpy.random.uniform(0.0, 1.0)
        # self.velocity = self.INERTIAL*self.velocity + self.COGNITIVE*r1*(self.bestPosition["fitness"]-self.position["fitness"])+self.SOCIAL*r2*(globalBest["fitness"]-self.position["fitness"])
        newSolution = []
        for i in self.position["solution"]:
            newSolution.append(i+self.INERTIAL*self.velocity + self.COGNITIVE*numpy.random.uniform(0.0, 1.0)*(self.bestPosition["fitness"]-self.position["fitness"])+self.SOCIAL*numpy.random.uniform(0.0, 1.0)*(globalBest["fitness"]-self.position["fitness"]))

        newFitness = antennaArray.evaluate(newSolution)
        while not antennaArray.is_valid(newSolution):
            for i in self.position["solution"]:
                newSolution.append(i + self.INERTIAL*self.velocity + self.COGNITIVE*numpy.random.uniform(0.0, 1.0)*(self.bestPosition["fitness"]-self.position["fitness"])+self.SOCIAL*numpy.random.uniform(0.0, 1.0)*(globalBest["fitness"]-self.position["fitness"]))

        if (newFitness > antennaArray.evaluate(self.bestPosition["solution"])):
            self.bestPosition["solution"] = newSolution
            self.bestPosition["fitness"] = antennaArray.evaluate(newSolution)
        self.position["solution"] = newSolution
        self.position["fitness"] = antennaArray.evaluate(newSolution)


def getGlobalBest(antennaArray,swarm):
    globalBest = {"solution":[],"fitness":0.0}
    for paritcle in swarm:
            globalBest["solution"] = paritcle.bestPosition["solution"]
            globalBest["fitness"] = paritcle.bestPosition["fitness"]
    return globalBest

def swarm(antennaArray,seconds):

    Swarm = []
    # initialPositions = ContinuousRandomSearch.generateSolution(antennaArray)["design"]
    # initialPositions.sort()
    for i in range(0,antennaArray.n_antennae):
        velocity = numpy.random.uniform(0.0,antennaArray.n_antennae/2)
        design = ContinuousRandomSearch.generateSolution(antennaArray)["design"]
        position = {"solution":design,"fitness":antennaArray.evaluate(design)}
        Swarm.append(Particle(velocity,position))
        # print 1

    globalPosition = getGlobalBest(antennaArray,Swarm)

    timeout = time.time() + seconds

    while time.time() < timeout:
        for paritcle in Swarm:
            paritcle.update(antennaArray,globalPosition)
            # print paritcle.SOCIAL
        globalPosition = getGlobalBest(antennaArray,Swarm)

    return globalPosition

antennaArray = AntennaArray.AntennaArray(5, 70.0)
print swarm(antennaArray,10)

# print numpy.random.uniform(0.0,1.0)


