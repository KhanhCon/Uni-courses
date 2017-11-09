import AntennaArray
import numpy
import random
import time
import threading
import bisect


antennaArray = AntennaArray.AntennaArray(10, 90.0)
design = [1.5,0.7,0.0]
# print len(design) == antennaArray.n_antennae
# print antennaArray.evaluate(design)

def generatingSolitions(antennaArray):
    fail = 0
    peak = float(antennaArray.n_antennae)/2
    design = [peak]
    # lowerBound = 0.0
    # upperBound = antennaArray.n_antennae/2
    ranges = [0.0,peak]
    for i in range(1,antennaArray.n_antennae):
        randomRange = range(1,len(ranges))
        index = numpy.random.randint(0,len(randomRange)-1)if len(randomRange) > 1 else 0
        rand = randomRange[index]
        # print rand
        lowerBound = 0.0 if ranges[rand-1] == 0.0 else ranges[rand-1]+antennaArray.MIN_SPACING
        upperBound = ranges[rand]-antennaArray.MIN_SPACING
        while upperBound < lowerBound:
            fail += 1
            del randomRange[index]
            index = numpy.random.randint(0, len(randomRange) - 1) if len(randomRange) > 1 else 0
            rand = randomRange[index]
            # print "repeat: " + str(rand)
            lowerBound = 0.0 if ranges[rand - 1] == 0.0 else ranges[rand - 1]+antennaArray.MIN_SPACING
            upperBound = ranges[rand]-antennaArray.MIN_SPACING

        node = numpy.random.uniform(lowerBound, upperBound)
        while node == lowerBound:
            node = numpy.random.uniform(lowerBound, upperBound)
        design.append(node)

        if node+antennaArray.MIN_SPACING>=ranges[-1]-antennaArray.MIN_SPACING:
            # ranges.remove(-1)
            del ranges[-1]

        if node-antennaArray.MIN_SPACING < 0.0:
            # ranges.remove(0)
            del ranges[0]
        elif node-antennaArray.MIN_SPACING < ranges[0]+antennaArray.MIN_SPACING:
            # ranges.remove(0)
            del ranges[0]

        # ranges.append(node)
        insert_point = bisect.bisect(ranges, node)
        ranges[insert_point:insert_point]=[node]
        # print "unsorted: " + str(ranges)
        # ranges.sort()
        # print "sorted:   " + str(ranges)

    return {"design":design, "fail":fail,"total":fail+antennaArray.n_antennae-1}

a = generatingSolitions(antennaArray)
print a
print antennaArray.is_valid(a["design"])
# print antennaArray.evaluate(a)
def f(f_stop,time=0,printInterval=2):
    # do something here ..
    # .

    if not f_stop.is_set():
        # call f() again in 60 seconds
        threading.Timer(printInterval, f, [f_stop,time+printInterval,printInterval]).start()
        print time

def randomSearch(antennaArray, seconds=10, printInterval=2):
    fail = 0
    total = 0
    smallestSLL = 10000
    bestDesign = None
    timeout = time.time() + seconds
    f_stop = threading.Event()
    f(f_stop, printInterval=printInterval)
    while time.time() < timeout:
        solution = generatingSolitions(antennaArray)
        design = solution["design"]
        fail += solution["fail"]
        total += solution["total"]
        SLL = antennaArray.evaluate(design)
        if smallestSLL > SLL:
            smallestSLL = SLL
            bestDesign = design

    f_stop.set()
    return {'design': bestDesign, 'smallest SLL': smallestSLL,'fail rate':round(100*fail/(total*1.0),2)}



def check():
    for i in range(100):
        if not antennaArray.is_valid(generatingSolitions(antennaArray)["design"]):
            print "Fail test"
    print "Test Passed: no invalid design generated"

check()
print randomSearch(antennaArray,5,1)