# import ContinuousRandomSearch
# import AntennaArray
# import time
# import numpy
#
# class Particle:
#     # swarmSize = 20+...
#     INERTIAL = 0.721
#     COGNITIVE = 1.1193
#     SOCIAL = 2.0
#     def __init__(self,velocity,position):
#         self.velocity = velocity
#         self.position = position
#         self.bestPosition = position
#     def update(self,antennaArray,globalBest):
#         # r1 = numpy.random.uniform(0.0, 1.0)
#         # r2 = numpy.random.uniform(0.0, 1.0)
#         # self.velocity = self.INERTIAL*self.velocity + self.COGNITIVE*r1*(self.bestPosition["fitness"]-self.position["fitness"])+self.SOCIAL*r2*(globalBest["fitness"]-self.position["fitness"])
#         newSolution = []
#         for i in self.position["geno1"]:
#             newSolution.append(i+self.INERTIAL*self.velocity + self.COGNITIVE*numpy.random.uniform(0.0, 1.0)*(self.bestPosition["fitness"]-self.position["fitness"])+self.SOCIAL*numpy.random.uniform(0.0, 1.0)*(globalBest["fitness"]-self.position["fitness"]))
#
#         newFitness = antennaArray.evaluate(newSolution)
#         while not antennaArray.is_valid(newSolution):
#             for i in self.position["geno1"]:
#                 newSolution.append(i + self.INERTIAL*self.velocity + self.COGNITIVE*numpy.random.uniform(0.0, 1.0)*(self.bestPosition["fitness"]-self.position["fitness"])+self.SOCIAL*numpy.random.uniform(0.0, 1.0)*(globalBest["fitness"]-self.position["fitness"]))
#
#         if (newFitness > antennaArray.evaluate(self.bestPosition["geno1"])):
#             self.bestPosition["geno1"] = newSolution
#             self.bestPosition["fitness"] = antennaArray.evaluate(newSolution)
#         self.position["geno1"] = newSolution
#         self.position["fitness"] = antennaArray.evaluate(newSolution)
#
#
# def getGlobalBest(antennaArray,swarm):
#     globalBest = {"geno1":[],"fitness":0.0}
#     for paritcle in swarm:
#             globalBest["geno1"] = paritcle.bestPosition["geno1"]
#             globalBest["fitness"] = paritcle.bestPosition["fitness"]
#     return globalBest
#
# def swarm(antennaArray,seconds):
#
#     Swarm = []
#     # initialPositions = ContinuousRandomSearch.generateSolution(antennaArray)["design"]
#     # initialPositions.sort()
#     for i in range(0,antennaArray.n_antennae):
#         velocity = numpy.random.uniform(0.0,antennaArray.n_antennae/2)
#         design = ContinuousRandomSearch.generateSolution(antennaArray)["design"]
#         position = {"geno1":design,"fitness":antennaArray.evaluate(design)}
#         Swarm.append(Particle(velocity,position))
#         # print 1
#
#     globalPosition = getGlobalBest(antennaArray,Swarm)
#
#     timeout = time.time() + seconds
#
#     while time.time() < timeout:
#         for paritcle in Swarm:
#             paritcle.update(antennaArray,globalPosition)
#             # print paritcle.SOCIAL
#         globalPosition = getGlobalBest(antennaArray,Swarm)
#
#     return globalPosition
#
# antennaArray = AntennaArray.AntennaArray(5, 70.0)
# print swarm(antennaArray,10)
#
# # print numpy.random.uniform(0.0,1.0)
#
#

import random
from operator import attrgetter
import random, sys, time, copy, threading
import lab1

class Particle:
    def __init__(self, solution, cost):
        # current geno1
        self.solution = solution

        # best geno1 (fitness) it has achieved so far
        self.pbest = solution

        # set costs
        self.cost_current_solution = cost
        self.cost_pbest_solution = cost

        # velocity of a particle is a sequence of 4-tuple
        # (1, 2, 1, 'beta') means SO(1,2), prabability 1 and compares with "beta"
        self.velocity = []

    # set pbest
    # def setPBest(self, new_pbest):
    #     self.pbest = new_pbest

    # returns the pbest
    # def getPBest(self):
    #     return self.pbest

    # set the new velocity (sequence of swap operators)
    # def setVelocity(self, new_velocity):
    #     self.velocity = new_velocity

    # returns the velocity (sequence of swap operators)
    # def getVelocity(self):
    #     return self.velocity

    # set geno1
    # def setCurrentSolution(self, geno1):
    #     self.geno1 = geno1

    # gets geno1
    # def getCurrentSolution(self):
    #     return self.geno1

    # set cost pbest geno1
    # def setCostPBest(self, cost):
    #     self.cost_pbest_solution = cost

    # gets cost pbest geno1
    # def getCostPBest(self):
    #     return self.cost_pbest_solution

    # set cost current geno1
    # def setCostCurrentSolution(self, cost):
    #     self.cost_current_solution = cost

    # gets cost current geno1
    # def getCostCurrentSolution(self):
    #     return self.cost_current_solution

    # removes all elements of the list velocity
    # def clearVelocity(self):
    #     del self.velocity[:]

def f(f_stop, time=0, printInterval=1):
    if not f_stop.is_set():
        # call f() again in 60 seconds
        threading.Timer(printInterval, f, [f_stop, time + printInterval, printInterval]).start()
        print time

# PSO algorithm
class PSO_TSP:
    def __init__(self, graph, iteration, size_population, beta=1, alfa=1):
        self.graph = graph  # the graph
        self.iteration = iteration  # max of iteration
        self.size_population = size_population  # size population
        self.particles = []  # list of particles
        self.beta = beta  # the probability that all swap operators in swap sequence (gbest - x(t-1))
        self.alfa = alfa  # the probability that all swap operators in swap sequence (pbest - x(t-1))

        # initialized with a group of random particles (solutions)
        # solutions = self.graph.getRandomPaths(self.size_population)
        solutions = []
        for i in range(1,size_population):
            route = list(graph.vertices)
            random.shuffle(route)
            solutions.append(route)

        # creates the particles and initialization of swap sequences in all the particles
        for solution in solutions:
            # creates a new particle
            particle = Particle(solution=solution, cost=lab1.getRouteCost(graph,solution))
            # add the particle
            self.particles.append(particle)

        # updates "size_population"
        self.size_population = len(self.particles)

    # set gbest (best particle of the population)
    # def setGBest(self, new_gbest):
    #     self.gbest = new_gbest

    # returns gbest (best particle of the population)
    # def getGBest(self):
    #     return self.gbest

    # shows the info of the particles
    def showsParticles(self):

        print('Showing particles...\n')
        for particle in self.particles:
            print('pbest: %s\t|\tcost pbest: %d\t|\tcurrent geno1: %s\t|\tcost current geno1: %d' \
                  % (str(particle.getPBest()), particle.getCostPBest(), str(particle.getCurrentSolution()),
                     particle.getCostCurrentSolution()))
        print('')

    def run(self):
        for i in range(self.iteration):
            # updates gbest (best particle of the population)
            self.gbest = min(self.particles, key=attrgetter('cost_pbest_solution'))

            # for each particle in the swarm
            for particle in self.particles:

                particle.velocity[:]  # cleans the speed of the particle
                temp_velocity = []
                solution_gbest = copy.copy(self.gbest.pbest)  # gets geno1 of the gbest
                solution_pbest = particle.pbest[:]  # copy of the pbest geno1
                solution_particle = particle.solution[:]  # gets copy of the current geno1 of the particle

                # generates all swap operators to calculate (pbest - x(t-1))
                for i in range(len(self.graph.vertices)):
                    if solution_particle[i] != solution_pbest[i]:
                        # generates swap operator
                        swap_operator = (i, solution_pbest.index(solution_particle[i]), self.alfa)

                        # append swap operator in the list of velocity
                        temp_velocity.append(swap_operator)

                        # makes the swap
                        aux = solution_pbest[swap_operator[0]]
                        solution_pbest[swap_operator[0]] = solution_pbest[swap_operator[1]]
                        solution_pbest[swap_operator[1]] = aux

                # generates all swap operators to calculate (gbest - x(t-1))
                for i in range(len(self.graph.vertices)):
                    if solution_particle[i] != solution_gbest[i]:
                        # generates swap operator
                        swap_operator = (i, solution_gbest.index(solution_particle[i]), self.beta)

                        # append swap operator in the list of velocity
                        temp_velocity.append(swap_operator)

                        # makes the swap
                        aux = solution_gbest[swap_operator[0]]
                        solution_gbest[swap_operator[0]] = solution_gbest[swap_operator[1]]
                        solution_gbest[swap_operator[1]] = aux

                # updates velocity
                particle.velocity = temp_velocity

                # generates new geno1 for particle
                for swap_operator in temp_velocity:
                    if random.random() <= swap_operator[2]:
                        # makes the swap
                        aux = solution_particle[swap_operator[0]]
                        solution_particle[swap_operator[0]] = solution_particle[swap_operator[1]]
                        solution_particle[swap_operator[1]] = aux

                # updates the current geno1
                particle.solution = solution_particle
                # gets cost of the current geno1
                cost_current_solution = lab1.getRouteCost(self.graph,solution_particle)
                # updates the cost of the current geno1
                particle.cost_current_solution = cost_current_solution

                # checks if current geno1 is pbest geno1
                if cost_current_solution < particle.cost_pbest_solution:
                    particle.pbest = solution_particle
                    particle.cost_pbest_solution = cost_current_solution


pso_tsp = PSO_TSP(lab1.TSP, iteration=10000, size_population=3, beta=1, alfa=1)
pso_tsp.run() # runs the PSO algorithm
print('gbest: %s | cost: %f\n' % (pso_tsp.gbest.pbest, pso_tsp.gbest.cost_pbest_solution))
