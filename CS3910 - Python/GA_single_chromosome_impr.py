import random, time, heapq, sys
from itertools import chain

l = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
     100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
     100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105,
     105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105,
     105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 110, 110,
     110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 115, 115, 115,
     115, 115, 115, 115, 115, 115, 115, 115, 115, 115]


class GA:
    class Genotype:
        def __init__(self, stock,piece, piece_map, price, chromosome, solution={}):
            self.chromosome = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 115, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120]

            self.piece_map = piece_map
            self.solution = solution
            for s in stock:
                self.solution[s] = []
            self.fitness = self.calculate_fitness_FFD(stock, price,piece)

        def BFD(self, stock_size, items,piece):
            def piece_sum(piece_map):
                total = 0
                for p in piece_map:
                    total += piece[p]
                return total

            bins = [[]]
            for item in items:  # Try reverse items reversed(items)
                fit = True
                for bin in bins:
                    if piece_sum(bin) + piece[item] <= stock_size:
                        bin.append(item)
                        fit = False
                        break
                if fit:
                    bins.append([item])
            bins.sort(key=lambda x: sum(x), reverse=True)
            # return self.lsearch(bins, 3, stock)
            return bins

        def FFD(self, stock_size, items):
            bins = [[]]

            for item in items:  # Try reverse items reversed(items)
                fit = True
                for bin in bins:
                    if sum(bin) + item <= stock_size:
                        bin.append(item)
                        fit = False
                        break
                if fit:
                    bins.append([item])
            # return self.lsearch(bins, 3, stock)
            return bins

        def calculate_fitness_FFD(self, stock, price,piece):
            cost = 0
            items = {}
            for s in stock:
                items[s] = []
            for i in xrange(0, len(self.chromosome)):
                items[self.chromosome[i]].append(self.piece_map[i])
            for key, value in items.iteritems():

                solution = self.BFD(key,value,piece)
                cost += len(solution)*price[key]
                phenotype_solution = []
                for bin in solution:
                    phenotype_bin = []
                    for item in bin:
                        phenotype_bin.append(piece[item])
                    phenotype_solution.append(phenotype_bin)
                self.solution[key] = phenotype_solution

            return cost

        def print_solution2(self, stock):
            items = {}

            pie = []
            quantities = []

            for s in stock:
                items[s] = []
            for i in xrange(0, len(self.chromosome)):
                items[self.chromosome[i]].append(self.piece[i])
            pieces = 0
            bin_p = 0
            for key, value in items.iteritems():
                pieces += len(value)
                bins = self.FFD(key, value)
                for bin in bins:
                    if sum(bin) > key:
                        print("Exceed: %s:  %s" % (key, bin))
                for i in bins:
                    bin_p += len(i)
                for bin in bins:
                    for item in bin:
                        pie.append(item)
                # print "%i: %s" % (key, value)
                print("%i: %s" % (key, bins))
            # print("chromosome: %s" % self.chromosome)
            print("cost: %s" % self.fitness)

        def print_solution(self, stock,piece):
            def piece_sum(piece_map):
                total = 0
                for p in piece_map:
                    total += piece[p]
                return total

            items = {}

            pie = []
            quantities = []

            for s in stock:
                items[s] = []
            for i in xrange(0, len(self.chromosome)):
                items[self.chromosome[i]].append(piece[i])
            pieces = 0
            bin_p = 0
            for key, value in items.iteritems():
                pieces += len(value)
                bins = self.FFD(key, value)
                for bin in bins:
                    if piece_sum(bin) > key:
                        print("Exceed: %s:  %s" % (key, bin))
                for i in bins:
                    bin_p += len(i)
                for bin in bins:
                    for item in bin:
                        pie.append(item)
                # print "%i: %s" % (key, value)
                print("%i: %s" % (key, bins))
            # print("chromosome: %s" % self.chromosome)
            print("cost: %s" % self.fitness)

    def __init__(self, stock, piece, price):
        self.solution = None
        self.stock = stock
        # random.shuffle(piece)
        # self.piece = piece
        self.piece = sorted(piece, reverse=True)
        self.price = price
        self.piece_map = range(0,len(piece))

    def random_geno(self):
        chromosome = [None] * len(self.piece_map)
        for i in xrange(0, len(self.piece_map)):
            chromosome[i] = random.choice(self.stock)
        geno_piece_map = []
        geno_piece_map[:] = self.piece_map [:]
        random.shuffle(geno_piece_map)

        # print chromosome
        geno = self.Genotype(self.stock,self.piece, geno_piece_map, self.price, chromosome)
        # geno.update_fitness(self.stock,self.piece,self.price)
        return geno

    def random_population(self, population_size):
        population = []
        for i in range(0, population_size):
            population.append(self.random_geno())
        return population

    def tournament_selection(self, population):
        tournament_population_size = random.randint(10, 20)
        tournament_population = random.sample(population, tournament_population_size)

        min1, min2 = heapq.nsmallest(2, tournament_population,  key=lambda x: x.fitness) #slowest

        # min1, min2 = sorted(tournament_population, key=lambda x: x.fitness)[0:2] #3rd slowest
        # tournament_population.sort(key=lambda x: x.fitness) #second slowest
        # min1, min2 = tournament_population[0:2]             #second slowest
        return [min1, min2]

    def inner_pmx_cross_over(self, parent_piece_map):
        # cross_point = random.randint(1, len(parent_piece_map[0])-1)

        def locate(original, pa2_item, parent1, parent2, crosspoint1, crosspoint2, child):

            item_index = parent2.index(pa2_item)
            pa1_same_index = parent1[item_index]
            pa2_index = parent2.index(pa1_same_index)
            if pa2_index < crosspoint2 and pa2_index >= crosspoint1:
                locate(original, parent2[pa2_index], parent1, parent2, crosspoint1, crosspoint2, child)
            else:
                child[pa2_index] = original

        cross_points = random.sample(xrange(len(parent_piece_map[0]) + 1), 2)

        cross_points.sort()
        # print cross_points
        child_piece_map1 = [None] * len(parent_piece_map[0])
        child_piece_map1[cross_points[0]:cross_points[1]] = parent_piece_map[0][cross_points[0]:cross_points[1]]
        for i in xrange(cross_points[0], cross_points[1]):
            if parent_piece_map[1][i] not in child_piece_map1:
                # value_same_index = locate(i, parent_piece_map[0])
                locate(parent_piece_map[1][i], parent_piece_map[1][i], parent_piece_map[0], parent_piece_map[1], cross_points[0], cross_points[1], child_piece_map1)
        for i in xrange(0, len(child_piece_map1)):
            if child_piece_map1[i] == None:
                child_piece_map1[i] = parent_piece_map[1][i]

        child_piece_map2 = [None] * len(parent_piece_map[1])
        child_piece_map2[cross_points[0]:cross_points[1]] = parent_piece_map[1][cross_points[0]:cross_points[1]]
        for i in xrange(cross_points[0], cross_points[1]):
            if parent_piece_map[0][i] not in child_piece_map2:
                # value_same_index = locate(i, parent_piece_map[0])
                locate(parent_piece_map[0][i], parent_piece_map[0][i], parent_piece_map[1], parent_piece_map[0], cross_points[0], cross_points[1], child_piece_map2)
        for i in xrange(0, len(child_piece_map2)):
            if child_piece_map2[i] == None:
                child_piece_map2[i] = parent_piece_map[0][i]

        # child_chromosome1 = []
        # child_chromosome1[:] = parent_chromosome[0][:]
        # child_chromosome2 = []
        # child_chromosome2[:] = parent_chromosome[1][:]
        #
        # geno1 = self.Genotype(self.stock, self.piece, child_piece_map1, self.price, child_chromosome1)
        # geno2 = self.Genotype(self.stock, self.piece, child_piece_map2, self.price, child_chromosome2)

        return child_piece_map1, child_piece_map2

    def uniform_crossover(self, parent_chromosome, parent_piece_map):
        child_chromosome = [[None] * len(parent_chromosome[0]), [None] * len(parent_chromosome[0])]
        child_piece = [[None] * len(parent_piece_map[0]), [None] * len(parent_piece_map[0])]
        for i in range(0, len(parent_chromosome[0])):
            if random.uniform(0, 1) < 0.5:
                child_chromosome[0][i] = parent_chromosome[0][i]
                child_chromosome[1][i] = parent_chromosome[1][i]

            else:
                child_chromosome[1][i] = parent_chromosome[0][i]
                child_chromosome[0][i] = parent_chromosome[1][i]

        # child_piece_map1 = []
        # child_piece_map1[:] = parent_piece_map[0][:]
        # child_piece_map2 = []
        # child_piece_map2[:] = parent_piece_map[1][:]
        child_piece_map1, child_piece_map2 = self.inner_pmx_cross_over(parent_piece_map)
        geno1 = self.Genotype(self.stock,self.piece, child_piece_map1, self.price, child_chromosome[0])
        geno2 = self.Genotype(self.stock,self.piece, child_piece_map2, self.price, child_chromosome[1])

        return geno1, geno2



    def pmx_cross_over(self, parent_chromosome, parent_piece_map):
        # cross_point = random.randint(1, len(parent_piece_map[0])-1)

        def locate(original, pa2_item, parent1, parent2, crosspoint1, crosspoint2, child):

            item_index = parent2.index(pa2_item)
            pa1_same_index = parent1[item_index]
            pa2_index = parent2.index(pa1_same_index)
            if pa2_index < crosspoint2 and pa2_index >= crosspoint1:
                locate(original, parent2[pa2_index], parent1, parent2, crosspoint1, crosspoint2, child)
            else:
                child[pa2_index] = original

        cross_points = random.sample(xrange(len(parent_piece_map[0]) + 1), 2)

        cross_points.sort()
        # print cross_points
        child_piece_map1 = [None] * len(parent_piece_map[0])
        child_piece_map1[cross_points[0]:cross_points[1]] = parent_piece_map[0][cross_points[0]:cross_points[1]]
        for i in xrange(cross_points[0], cross_points[1]):
            if parent_piece_map[1][i] not in child_piece_map1:
                # value_same_index = locate(i, parent_piece_map[0])
                locate(parent_piece_map[1][i], parent_piece_map[1][i], parent_piece_map[0], parent_piece_map[1], cross_points[0], cross_points[1], child_piece_map1)
        for i in xrange(0, len(child_piece_map1)):
            if child_piece_map1[i] == None:
                child_piece_map1[i] = parent_piece_map[1][i]

        child_piece_map2 = [None] * len(parent_piece_map[1])
        child_piece_map2[cross_points[0]:cross_points[1]] = parent_piece_map[1][cross_points[0]:cross_points[1]]
        for i in xrange(cross_points[0], cross_points[1]):
            if parent_piece_map[0][i] not in child_piece_map2:
                # value_same_index = locate(i, parent_piece_map[0])
                locate(parent_piece_map[0][i], parent_piece_map[0][i], parent_piece_map[1], parent_piece_map[0], cross_points[0], cross_points[1], child_piece_map2)
        for i in xrange(0, len(child_piece_map2)):
            if child_piece_map2[i] == None:
                child_piece_map2[i] = parent_piece_map[0][i]

        child_chromosome1 = []
        child_chromosome1[:] = parent_chromosome[0][:]
        child_chromosome2 = []
        child_chromosome2[:] = parent_chromosome[1][:]

        geno1 = self.Genotype(self.stock, self.piece, child_piece_map1, self.price, child_chromosome1)
        geno2 = self.Genotype(self.stock, self.piece, child_piece_map2, self.price, child_chromosome2)

        return geno1, geno2

    def scramble_mutation(self, parent_chromosome,parrent_piece_map):
        child_chromosome = []
        child_chromosome[:] = parent_chromosome[:]

        random_indexes = random.sample(xrange(0, len(child_chromosome) - 1), 2)

        # ranl = random.sample(xrange(0, len(STOCK)), 2)

        for i in xrange(random_indexes[0], random_indexes[1]):
            ranl = random.randint(0, len(self.stock) - 1)
            child_chromosome[i] = self.stock[ranl]

        # random.shuffle(parrent_piece_map)

        return self.Genotype(self.stock,self.piece, parrent_piece_map, self.price, child_chromosome)

    def run(self, iteration, population_size=50, mutation_rate=0.8):
        print("running EA_stock_cutting...")
        mutation_rate = mutation_rate
        population = self.random_population(population_size)
        # population.sort(key=lambda x:x.fitness)
        best_geno = None
        best_fitness = 100000
        count = 0

        start_time = time.time()
        for iter in range(1, iteration + 1):
            newGen = []
            # population_size
            new_len = random.randint(4, 5)
            while len(newGen) < population_size:

                prob = random.uniform(0, 1)
                if prob < mutation_rate:
                    index = random.randint(0, len(population) - 1)
                    newGen.append(self.scramble_mutation(population[index].chromosome,population[index].piece_map))
                else:
                    parents = self.tournament_selection(population)
                    ran = random.randint(0,1)

                    children = self.pmx_cross_over([parents[0].chromosome, parents[1].chromosome],[parents[0].piece_map, parents[1].piece_map])
                    # children = self.uniform_crossover([parents[0].chromosome, parents[1].chromosome],[parents[0].piece_map, parents[1].piece_map])

                    newGen.append(children[0])
                    if children[0].chromosome != children[1].chromosome:
                        newGen.append(children[1])

            if random.uniform(0, 1) < 1:
                population[:] = newGen[:]
            else:
                population = population + newGen
                # print len(population)
                population.sort(key=lambda x: x.fitness)
                del population[-population_size:]

            sys.stdout.write('\r')
            sys.stdout.write("iteration: %s || seconds: %s || mutation rate: %s" % (str(iter), time.time() - start_time, str(mutation_rate)))
            if iter % 10 == 0:
                if (population[0].fitness < best_fitness):
                    best_geno = population[0]
                    best_fitness = population[0].fitness
                    count = 0
                    #
                    #     if count >= 11:
                    #         # break
                    #         0
                    #     count += 1
                    #
                    #     print('\n')
                    #     print "*****"
                    #     population.sort(key=lambda x: x.fitness)


                    # print population[0].fitness
                    # print "*****"
        # sys.stdout.write('\n')


        # population.sort(key=lambda x: x.fitness)
        # best = population[0]
        print ""
        best = min(population, key=lambda x: x.fitness)
        if best.fitness > best_geno.fitness:
            best = best_geno

        # best.print_solution(self.stock, self.piece)
        for key, value in best.solution.iteritems():
            print("%i: %s" % (key, value))

        self.solution = best
        print "cost %s" % best.fitness
        return best

    def random_search(self, iteration, max_time):
        print 'Running random search...'
        repeated = set()
        best_fitness = 10000
        best_geno = None
        start = time.time()
        while best_fitness > 1800:
            # while time.time() - start < float(max_time):
            # for i in xrange(0,iteration):
            random_geno = self.random_geno()
            chromosome_string = int(''.join(str(elem) for elem in random_geno.chromosome))
            if chromosome_string in repeated:
                print "REPEATED"
                continue
            if random_geno.fitness < best_fitness:
                best_fitness = random_geno.fitness
                best_geno = random_geno
            repeated.add(chromosome_string)
            sys.stdout.write('\r')
            sys.stdout.write("seconds: %s " % (time.time() - start))

            if time.time() - start > float(100):
                break
        sys.stdout.write('\r')
        print "random seartch cost: %s" % best_geno.fitness


if __name__ == '__main__':
    price1 = {10: 100, 13: 130, 15: 150}
    stock1 = (10, 13, 15)
    piece1 = [3, 3, 3, 3, 3, 4, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10, 10, 10]
    # ,        [10, 10, 15 ,13
    price2 = {4300: 86, 4250: 85, 4150: 83, 3950: 79, 3800: 68, 3700: 66, 3550: 64, 3500: 63}
    stock2 = (4300, 4250, 4150, 3950, 3800, 3700, 3550, 3500)
    piece2 = [2350, 2350, 2250, 2250, 2250, 2250, 2200, 2200, 2200, 2200, 2100, 2100, 2100, 2100, 2100, 2100, 2100,
              2100,
              2100, 2100, 2100, 2100, 2100, 2100, 2100, 2050, 2050, 2050, 2050, 2050, 2050, 2000, 2000, 2000, 2000,
              2000,
              2000, 2000, 2000, 2000, 2000, 2000, 1950, 1950, 1950, 1950, 1950, 1950, 1900, 1900, 1900, 1900, 1900,
              1900,
              1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850,
              1850,
              1850, 1850, 1850, 1850, 1700, 1700, 1700, 1700, 1700, 1650, 1650, 1350, 1350, 1350, 1350, 1350, 1350,
              1350,
              1350, 1350, 1300, 1300, 1300, 1250, 1250, 1250, 1250, 1250, 1250, 1200, 1200, 1200, 1200, 1200, 1200,
              1200,
              1200, 1200, 1200, 1150, 1150, 1150, 1150, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1050, 1050,
              1050]

    stock3 = (120, 115, 110, 105, 100)
    price3 = {120: 12, 115: 11.5, 110: 11, 105: 10.5, 100: 10}
    piece3 = [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
              22, 22, 24, 24, 24, 24, 24, 24, 24, 25, 25, 25, 25, 25, 27, 27, 27, 27, 27, 27, 27, 27, 27, 29, 29, 29,
              29, 29, 29, 29, 29, 29, 30, 30, 30, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 32, 32,
              32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33,
              33, 33, 33, 33, 33, 33, 33, 34, 34, 34, 34, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35,
              35, 35, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 39, 39, 39, 39,
              39, 39, 39, 39, 39, 42, 42, 42, 42, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44,
              44, 44, 45, 45, 45, 45, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 47, 47, 47, 47, 47, 47, 47, 47,
              47, 47, 47, 47, 47, 47, 47, 48, 48, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49,
              49, 49, 49, 49, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 51, 51, 51, 51, 51, 51, 51, 51,
              51, 51, 51, 51, 51, 51, 51, 52, 52, 52, 52, 52, 52, 53, 53, 53, 53, 54, 54, 54, 54, 54, 54, 54, 55, 55,
              55, 55, 55, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 57, 57, 57, 57,
              57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 59, 59, 59, 59, 59, 59, 60, 60, 60, 61, 61,
              61, 61, 61, 61, 61, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 65,
              65, 65, 65, 65, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67,
              67, 67, 67, 67, 67]

    GA = GA(stock3, piece3, price3)

    start_time = time.time()
    geno = GA.run(iteration=50, population_size=200, mutation_rate=0.0)
    print("---GA runtime: %s seconds --- \n" % (time.time() - start_time))


    # start_time = time.time()
    # GA.random_search(1,100)
    # print("---Random Search runtime: %s seconds ---" % (time.time() - start_time))
    # stock_size = 13
    # piece = [7, 7, 7, 6, 6, 3, 3]
    # price = 130
    #
    # piece = [8, 7, 9, 6]
    # stock_size = 15
    # price = 150
    #

    # piece = [2350, 1150, 2000, 1200, 2100, 1350, 2250, 1200, 2100, 1350, 2350, 1050, 2100, 1250, 2000, 1250, 2200, 1250, 2200,
    #  1300, 1100, 1100, 1050, 2100, 1100, 2050, 1100, 2250, 1050, 2100, 1350, 2100, 1300, 2000, 1200, 2000, 1200, 2000,
    #  1200, 2100, 1200, 2050, 1350, 2050, 1350, 2250, 1250, 2100, 1200, 2250, 1250, 2100, 1350, 2050, 1350, 1100, 1100,
    #  1100, 2000, 1300, 1250, 1150, 1100, 2100, 1200, 2100, 1200, 1200, 1150, 1150]
    # stock_size = 3500
    # price = 63



    # ga_group = GA_group(piece=piece,price=price,stock_size=stock_size)
    # geno, fitness = ga_group.run(10,30,0.2)
    # geno.print_solution(piece)
    # print geno.chromosome
    # print geno.fitness



    # solution = ga_group.random_population(1)
    # print solution[0].chromosome
    # print ga_group.piece
