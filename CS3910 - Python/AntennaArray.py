import numpy
import math


class AntennaArray:

    MIN_SPACING = 0.25

    def __init__(self,n_ant,steering_ang):
        self.n_antennae = n_ant
        self.steering_angle = steering_ang


    def bounds(self):
        bnds = [[0 for x in range(2)] for y in range(self.n_antennae)]
        dim_bnd = [0.0,float(self.n_antennae)/2]
        for i in range(self.n_antennae):
            bnds[i] = dim_bnd
        return bnds

    def is_valid(self,design):
        if(len(design) != self.n_antennae):
            return False
        des = []
        des = design[:]
        des.sort()

        if(abs(des[-1]-(float(self.n_antennae)/2.0))>1e-10):
            # print "false"
            return False
        for i in range(len(des)):
            if(des[i] < self.bounds()[i][0] or des[i] > self.bounds()[i][1]):
                return False
        for i in range(len(des)-1):
            if(des[i+1]-des[i]<self.MIN_SPACING):
                return False
        return True

    def array_factor(self,design,elevation):
        steering = 2.0 * math.pi * self.steering_angle / 360.0
        elevation = 2.0 * math.pi * elevation / 360.0
        sum = 0.0
        for x in design:
            sum += math.cos(2 * math.pi * x * (math.cos(elevation) - math.cos(steering)))

        return 20.0 * math.log(abs(sum))


    def evaluate(self,design):
        if(len(design)!= self.n_antennae):
            raise ValueError("AntennaArray::evaluate called on design of the wrong size. Expected: " + str(self.n_antennae) +". Actual: " +str(len(design)))

        if (not self.is_valid(design)):
            return float("inf")

        class PowerPeak:
            # elevation = float
            # power = float
            def __init__ (self,e,p):
                self.elevation = e
                self.power = p

        peaks = []
        prev = PowerPeak(0.0,float("-inf"))
        current = PowerPeak(0.0, self.array_factor(design, 0.0))
        for elevation in numpy.arange(0.01, 180.0, 0.01):
            next = PowerPeak(elevation, self.array_factor(design, elevation))
            if (current.power >= prev.power and current.power >= next.power):
                peaks.append(current)
            prev = current
            current = next
        peaks.append(PowerPeak(180.0, self.array_factor(design, 180.0)))
        peaks.sort(key=lambda x: x.power, reverse=True)
        if (len(peaks) < 2):
            return float('-inf')
        distance_from_steering = abs(peaks[0].elevation - self.steering_angle)
        for i in range(1,len(peaks)):
            if (abs(peaks[i].elevation - self.steering_angle) < distance_from_steering):
                return peaks.get(0).power

        return peaks[1].power



# bar = range(10,1,-1)
# bar.sort()
# print bar
# class PowerPeak:
#     # elevation = float
#     # power = float
#     def __init__ (self,e,p):
#         self.elevation = e
#         self.power = p
# PowerPeak(1.0,5.0)
# peaks = []
# peaks.append(PowerPeak(1.0,1.0))
# peaks.append(PowerPeak(1.0,5.0))
# peaks.append(PowerPeak(1.0,3.0))
# for i in peaks:
#     print i.power
# peaks.sort(key=lambda x: x.power, reverse=True)
# for i in peaks:
#     print i.power
