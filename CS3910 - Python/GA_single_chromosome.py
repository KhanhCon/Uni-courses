import random, time, heapq, sys
from itertools import chain


class GA:
    class Genotype:
        def __init__(self, stock, piece, price, chromosome):
            self.chromosome = chromosome
            self.fitness = self.calculate_fitness_FFD(stock, piece, price)

        def replace(self, free_items, bins, bin_capacity):
            for bin in bins:
                waste = bin_capacity - sum(bin)
                if waste == 0:
                    continue
                for i1 in xrange(0, len(free_items)):
                    bre = False
                    for i2 in xrange(0, len(free_items)):
                        if i1 == i2:
                            continue
                        # i2_bre = False
                        for b1 in xrange(0, len(bin)):
                            # b1_bre = False
                            for b2 in xrange(0, len(bin)):
                                if b1 == b2:
                                    continue
                                improve22 = free_items[i1] + free_items[i2] - bin[b1] - bin[b2]
                                if bin_capacity - sum(bin) >= improve22 and improve22 > 0:
                                    free_items[i1], bin[b1], = bin[b1], free_items[i1],
                                    free_items[i2], bin[b2] = bin[b2], free_items[i2]
                                    free_items.sort(reverse=True)
                                    bre = True
                                    break
                                improve21 = free_items[i1] - bin[b2] - bin[b1]
                                if (bin_capacity - sum(bin) >= improve21 and improve21 > 0):
                                    free_items[i1], bin[b1], = bin[b1], free_items[i1]
                                    free_items.append(bin[b2])
                                    del bin[b2]
                                    free_items.sort(reverse=True)
                                    bre = True
                                    break
                                improve11 = free_items[i1] - bin[b1]
                                if (bin_capacity - sum(bin) >= improve11 and improve11 > 0):
                                    free_items[i1], bin[b1], = bin[b1], free_items[i1],
                                    free_items.sort(reverse=True)
                                    bre = True
                                    break
                            if bre: break
                        if bre: break
                    if bre: break



        def lsearch(self, bins, num_of_free_bin, bin_capacity):
            def FFD(stock_size, items):
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

                return bins

            if len(bins) == 1:
                return bins
            #
            # x[2] if len(x) > 2 else 0, x[3] if len(x) > 3 else 0

            bins.sort(
                key=lambda x: (sum(x), x[0]),
                reverse=True)

            original_len = len(bins)
            original_bins = []
            original_bins[:] = bins[:]
            free_items = sorted(chain(*bins[-num_of_free_bin:]), reverse=True)
            del bins[-num_of_free_bin:]
            bins.sort(key=lambda x: (sum(x), x[0]), )
            self.replace(free_items, bins, bin_capacity)
            free_items = sorted(free_items, reverse=True)
            # bins.append(FFD(bin_capacity, free_items))

            for bin in FFD(bin_capacity, free_items):
                if bin:
                    bins.append(bin)

            improved_len = len(bins)
            if (improved_len > original_len):
                print "ECHO!!"
                return original_bins
                # sys.exit()
            if improved_len < original_len:
                return self.lsearch(bins, num_of_free_bin, bin_capacity)
                # elif(improved_len > original_len):
                #     # return [[None]*original_len]
                #     0
                print "improve!!"
            else:
                return bins

        def BFD(self, stock_size, items):
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
            bins.sort(key=lambda x:sum(x),reverse=True)
            # return self.lsearch(bins, 3, stock_size)
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
            # return self.lsearch(bins, 3, stock_size)
            return bins

        def calculate_fitness_FFD(self, stock, piece, price):
            cost = 0
            items = {}
            for s in stock:
                items[s] = []
            for i in xrange(0, len(self.chromosome)):
                items[self.chromosome[i]].append(piece[i])
            for key, value in items.iteritems():
                cost += len(self.FFD(key, value)) * price[key]
            return cost

        def print_solution(self, stock, piece):
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

            # print("--------")
            #
            # print("Piece lengths: %s" % (sorted(list(set(pie)))))
            #
            # for p in sorted(set(pie)):
            #     quantities.append(pie.count(p))
            # print("Quantities:    %s" % quantities)
            #
            # print (bin_p)
            # print (pieces)

    def __init__(self, stock, piece, price):
        self.solution = None
        self.stock = stock
        # random.shuffle(piece)
        # self.piece = piece
        self.piece = sorted(piece, reverse=True)
        self.price = price

    def random_geno(self):
        chromosome = [None] * len(self.piece)
        for i in xrange(0, len(self.piece)):
            chromosome[i] = random.choice(self.stock)

        # print chromosome
        geno = self.Genotype(self.stock, self.piece, self.price, chromosome)
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

        m1, m2 = float('inf'), float('inf')
        min1, min2 = [], []
        for x in tournament_population:
            x_fitness = x.fitness
            if x_fitness <= m1:
                min1, min2 = x, min1
                m1, m2 = x_fitness, m1
            elif x_fitness < m2:
                min2 = x
                m2 = x_fitness

        # min1, min2 = heapq.nsmallest(2, tournament_population,  key=lambda x: x.fitness) #slowest

        # min1, min2 = sorted(tournament_population, key=lambda x: x.fitness)[0:2] #3rd slowest
        # tournament_population.sort(key=lambda x: x.fitness) #second slowest
        # min1, min2 = tournament_population[0:2]             #second slowest
        return [min1, min2]

    def uniform_crossover(self, parent_chromosome):
        child_chromosome = [[None] * len(parent_chromosome[0]), [None] * len(parent_chromosome[0])]
        for i in range(0, len(parent_chromosome[0])):
            if random.uniform(0, 1) < 0.5:
                child_chromosome[0][i] = parent_chromosome[0][i]
                child_chromosome[1][i] = parent_chromosome[1][i]
            else:
                child_chromosome[1][i] = parent_chromosome[0][i]
                child_chromosome[0][i] = parent_chromosome[1][i]

        geno1 = self.Genotype(self.stock, self.piece, self.price, child_chromosome[0])
        geno2 = self.Genotype(self.stock, self.piece, self.price, child_chromosome[1])

        return geno1, geno2

    def scramble_mutation(self, parent_chromosome):
        child_chromosome = []
        child_chromosome[:] = parent_chromosome[:]

        random_indexes = random.sample(xrange(0, len(child_chromosome) - 1), 2)

        # ranl = random.sample(xrange(0, len(STOCK)), 2)

        for i in xrange(random_indexes[0], random_indexes[1]):
            ranl = random.randint(0, len(self.stock) - 1)
            child_chromosome[i] = self.stock[ranl]

        return self.Genotype(self.stock, self.piece, self.price, child_chromosome)



    def run(self, iteration, population_size=50, mutation_rate=0.1):
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
                    newGen.append(self.scramble_mutation(population[index].chromosome))
                else:
                    parents = self.tournament_selection(population)
                    children = self.uniform_crossover([parents[0].chromosome, parents[1].chromosome])
                    newGen.append(children[0])
                    if children[0].chromosome != children[1].chromosome:
                        newGen.append(children[1])

            if random.uniform(0,1)<1:
                population[:] = newGen[:]
            else:
                population = population+newGen
                # print len(population)
                population.sort(key=lambda x:x.fitness)
                del population[-population_size:]

            sys.stdout.write('\r')
            sys.stdout.write("iteration: %s || seconds: %s || mutation rate: %s" % (str(iter), time.time() - start_time,str(mutation_rate)))
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


        population.sort(key=lambda x: x.fitness)
        best = population[0]
        if best.fitness > best_geno.fitness:
            best = best_geno
        # best = None
        # lowest = 10000
        # for geno in population:
        #     cost = geno.fitness
        #     if cost < lowest:
        #         best = geno
        #         lowest = cost
        # print_solution(stock, piece, price, best)
        # best.print_solution(self.stock, self.piece)
        print "cost: %s"%best.fitness

        # print lowest
        self.solution = best
        return best
    def random_search(self,iteration,max_time):
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
        print "random seartch cost: %s"%best_geno.fitness



if __name__ == '__main__':
    price1 = {10: 100, 13: 130, 15: 150}
    stock1 = (10, 13, 15)
    piece1 = [3, 3, 3, 3, 3, 4, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10, 10, 10]
    # ,        [10, 10, 15 ,13
    price2 = {4300: 86, 4250: 85, 4150: 83, 3950: 79, 3800: 68, 3700: 66, 3550: 64, 3500: 63}
    stock2 = (4300,4250, 4150, 3950, 3800, 3700, 3550,3500)
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
    geno = GA.run(iteration=500, population_size=100, mutation_rate=0.05)
    print("---GA runtime: %s seconds --- \n" % (time.time() - start_time))
    start_time = time.time()
    GA.random_search(1,100)
    print("---Random Search runtime: %s seconds ---" % (time.time() - start_time))
