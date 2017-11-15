import random, time
import AntennaArray
from ContinuousRandomSearch import generateSolution

class Particle:
    def __init__(self, antennaArray, position):
        # current solution
        self.antennaArray = antennaArray
        self.position = position # current positon
        self.PBest = position # personal best position
        self.cost_current = antennaArray.evaluate(position) # current cost
        self.cost_PBest = self.cost_current # personal best cost
        self.velocity = []
        for i in range(self.antennaArray.n_antennae):
            self.velocity.append(random.uniform(0, 1.0))

    def update(self, GBest):
        w = 0.721  # inertia constant
        c1 = 1.1193  # cognative constant
        c2 = 1.1193  # social constant

        for i in range(0, self.antennaArray.n_antennae):
            r1 = random.random()
            r2 = random.random()
            vel_cognitive = c1 * r1 * (self.PBest[i] - self.position[i])
            vel_social = c2 * r2 * (GBest[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + vel_cognitive + vel_social

        for i in range(1,self.antennaArray.n_antennae):
            self.position[i] = self.position[i] + self.velocity[i]
            if self.position[i] > self.antennaArray.bounds()[i][1]:
                self.position[i] = self.antennaArray.bounds()[i][1]
            if self.position[i] < self.antennaArray.bounds()[i][0]:
                self.position[i] = self.antennaArray.bounds()[i][0]
        self.position.sort()
        self.cost_current = self.antennaArray.evaluate(self.position)

        if self.antennaArray.is_valid(self.position) and self.cost_current<self.cost_PBest:
            self.PBest = self.position[:]
            self.cost_PBest = self.cost_current

def PSO(antennaArray,iteration,swarmSize):
    particles = []
    antennaArray = antennaArray
    GBest = []
    GBest_cost = 100000
    for i in range(0,swarmSize):
        particles.append(Particle(antennaArray, generateSolution(antennaArray)["design"]))

    print "Running PSO..."
    timeout = time.time()
    for i in range(iteration):

        for particle in particles:
            if GBest_cost > particle.cost_PBest:
                GBest = particle.PBest[:]
                GBest_cost = particle.cost_PBest

        for particle in particles:
            particle.update(GBest)
    print "Time running: %ss" % int(time.time() - timeout)
    print "Particles: "
    for particle in particles:
            particle.PBest =  ['%.2f' % elem for elem in particle.PBest]
            particle.PBest =  [float(elem) for elem in particle.PBest]
            particle.position =  ['%.2f' % elem for elem in particle.position]
            particle.position =  [float(elem) for elem in particle.position]
            particle.cost_current = '%.2f' % particle.cost_current
            particle.cost_PBest = '%.2f' % particle.cost_PBest
    for particle in particles:
        print "PBest   : %s, cost: %s | Position: %s, cost: %s" % (particle.PBest,particle.cost_PBest,particle.position,particle.cost_current)
    print ""
    print "Best position: "
    print {"GBest":GBest,"GBest_cost":GBest_cost,"test":antennaArray.evaluate(GBest)}

antenna = AntennaArray.AntennaArray(5,70.0)
PSO(antenna,iteration=500,swarmSize=5)






