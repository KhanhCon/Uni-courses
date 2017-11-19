import AntennaArray
import numpy
import random
import time
import threading
import bisect



# print len(design) == antennaArray.n_antennae
# print antennaArray.evaluate(design)

def generateSolution(antennaArray):
    fail = 0
    peak = float(antennaArray.n_antennae)/2
    design = [peak]

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
            lowerBound = 0.0 if ranges[rand - 1] == 0.0 else ranges[rand - 1]+antennaArray.MIN_SPACING
            upperBound = ranges[rand]-antennaArray.MIN_SPACING

        node = numpy.random.uniform(lowerBound, upperBound)
        while node == lowerBound:
            node = numpy.random.uniform(lowerBound, upperBound)
        # design.append(node)
        point = bisect.bisect(design,node)
        design[point:point]=[node]
        if node+antennaArray.MIN_SPACING>=ranges[-1]-antennaArray.MIN_SPACING:
            del ranges[-1]

        if node-antennaArray.MIN_SPACING < 0.0:
            del ranges[0]
        elif node-antennaArray.MIN_SPACING < ranges[0]+antennaArray.MIN_SPACING:
            del ranges[0]


        insert_point = bisect.bisect(ranges, node)
        ranges[insert_point:insert_point]=[node]


    return {"design":design, "fail":fail,"total":fail+antennaArray.n_antennae-1}

# antennaArray = AntennaArray.AntennaArray(5,90.0)
# a = generateSolution(antennaArray)
# print a
# print antennaArray.is_valid(a["design"])
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
        solution = generateSolution(antennaArray)
        design = solution["design"]
        fail += solution["fail"]
        total += solution["total"]
        SLL = antennaArray.evaluate(design)
        if smallestSLL > SLL:
            smallestSLL = SLL
            bestDesign = design

    f_stop.set()
    return {'design': bestDesign, 'smallest SLL': smallestSLL,'failure rate':round(100*fail/(total*1.0),2)}



# def check():
#     for i in range(100):
#         if not antennaArray.is_valid(generateSolution(antennaArray)["design"]):
#             print "Fail test"
#     print "Test Passed: no invalid design generated"

# check()
# antennaArray = AntennaArray.AntennaArray(5, 70.0)
# print randomSearch(antennaArray,seconds=5,printInterval=1)