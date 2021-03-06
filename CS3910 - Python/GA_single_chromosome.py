import random, time, heapq, sys
from itertools import chain


class GA_group:
    class Genotype:
        def __init__(self, chromosome, stock_size, price, piece):
            self.chromosome = chromosome
            self.fitness = len(chromosome) * price
            self.stock_size = stock_size
            self.price = price

        def print_solution(self, piece):
            solution = {}
            solution[self.stock_size] = []
            for i in xrange(0, len(self.chromosome)):
                pheno_bin = []
                for item in self.chromosome[i]:
                    pheno_bin.append(piece[item])
                solution[self.stock_size].append(pheno_bin)

            # piece_test = []
            # for key, value in solution.iteritems():
            #     piece_test.append(list(chain(*value)))
            #     for val in value:
            #         if sum(val) > key:
            #             print "Exceed"
            # piece_test = sorted(chain(*piece_test), reverse=False)
            # if piece_test == piece:
            #     print "Check piece: Passed"
            # else:
            #     print "Check piece: Failed"
            #     print piece_test

            for key, value in solution.iteritems():
                print "%s: %s" % (key, value)

    def __init__(self, stock_size, piece, price):
        self.stock = stock_size
        self.piece = piece
        self.price = price
        self.piece_map = range(0, len(piece))

    def FFD(self, items):
        def piece_sum(pieces):
            total = 0
            for p in pieces:
                total += self.piece[p]
            return total

        bins = [[]]
        for item in items:  # Try reverse items reversed(items)
            fit = True
            for bin in bins:
                if piece_sum(bin) + self.piece[item] <= self.stock:
                    bin.append(item)
                    fit = False
                    break
            if fit:
                bins.append([item])
        # return self.lsearch(bins, 3, stock)
        return bins

        # item_chromosome, stock, piece, price

    def mutation(self, item_chromosome):
        num_of_bins = random.randint(1, len(item_chromosome))

        mutating_pieces = []
        child = []
        child[:] = item_chromosome[:]
        for i in xrange(0, num_of_bins):
            bin = random.choice(child)
            try:
                mutating_pieces += bin
            except TypeError:
                print item_chromosome
            child.remove(bin)
        mutating_pieces.sort()
        child += self.FFD(mutating_pieces)

        geno = self.Genotype(child, self.stock, self.price, self.piece)
        # geno.update_stock(self.stock, self.piece, self.price)
        return geno

    def crossover(self, item_chromosome1, item_chromosome2):

        def in_list_of_list(item, lists):
            isIn = False
            for i in lists:
                if item in i:
                    isIn = True
                    break
            return isIn

        def rm_duplicates(items, seen):

            deleted_items = []
            deleted_groups = []

            for l in xrange(0, len(items)):
                acc_rm = []
                group = items[l]
                delete = False
                try:
                    li = range(0, len(group))
                except TypeError:
                    print "group: %s" % group
                    print "items: %s" % items
                for item in li:  # set(items[l]):#don't need set because lists doesn't have duplicates
                    # print deleted_by_acc
                    if not in_list_of_list(group[item], seen):
                        acc_rm.append(item)
                    else:
                        delete = True
                if delete:
                    deleted_groups.append(l)
                    for index in acc_rm:
                        deleted_items.append(group[index])
                        # deleted_items + acc_rm

            deleted_groups.sort(reverse=True)
            for item in deleted_groups:
                del items[item]

            if not items:
                items = seen
            else:
                insertpoint1 = random.randint(0, len(items) - 1)
                items[insertpoint1:insertpoint1] = seen
            return [deleted_items, items]

        # print item_chromosome1
        child1 = []
        child2 = []
        child1[:] = item_chromosome1[:]
        child2[:] = item_chromosome2[:]

        # try:
        if len(item_chromosome1) <= 2:
            crosspoint1 = [0, 1]
        else:
            crosspoint1 = sorted(random.sample(xrange(0, len(item_chromosome1) - 1), 2))

        if len(item_chromosome2) <= 2:
            crosspoint2 = [0, 1]
        else:
            crosspoint2 = sorted(random.sample(xrange(0, len(item_chromosome2) - 1), 2))

        # except ValueError:
        #     print item_chromosome1
        #     print item_chromosome2
        try:
            rm_dup1 = rm_duplicates(child2, seen=item_chromosome1[crosspoint1[0]:crosspoint1[1]])
            rm_dup2 = rm_duplicates(child1, seen=item_chromosome2[crosspoint2[0]:crosspoint2[1]])
        except TypeError:
            print crosspoint1
            print crosspoint2

        child1 = rm_dup2[1]
        child2 = rm_dup1[1]

        # insertpoint1 = random.randint(0, len(child1)-1)
        # child1[insertpoint1:insertpoint1] = item_chromosome2[crosspoint2[0]:crosspoint2[1]]

        if len(rm_dup2[0]) > 0:
            rm_dup2[0].sort()
            chro1 = self.FFD(rm_dup2[0])
            child1 += chro1

        if len(rm_dup1[0]) > 0:
            rm_dup1[0].sort()
            chro2 = self.FFD(rm_dup1[0])
            child2 += chro2

        geno1 = self.Genotype(child1, self.stock, self.price, self.piece)
        # geno1.update_stock(self.stock, self.piece, self.price)
        geno2 = self.Genotype(child2, self.stock, self.price, self.piece)
        # geno2.update_stock(self.stock, self.piece, self.price)

        return geno1, geno2

    def random_solution(self, geno, piece_mapping):
        copy_piece_mapping = []
        copy_piece_mapping[:] = piece_mapping[:]
        random.shuffle(copy_piece_mapping)
        geno.chromosome = self.FFD(copy_piece_mapping)
        geno.fitness = len(geno.chromosome) * geno.price

        # geno.update_stock(self.stock, self.piece, self.price)
        # solution.append({"length": random_stock, "solution_pieces": solution_pieces})
        return geno

    def random_population(self, population_size, ):
        population = []
        for i in xrange(0, population_size):
            population.append(
                self.random_solution(self.Genotype([], self.stock, self.price, self.piece), self.piece_map))
        return population

    def tournament_selection(self, geno_population):
        tournament_population_size = random.randint(2, 3)
        tournament_population = random.sample(geno_population, tournament_population_size)

        min1, min2 = heapq.nsmallest(2, tournament_population, key=lambda x: x.fitness)
        return min1, min2

    def run(self, iteration, population_size=50, mutation_rate=0.00):
        # print "running EA_stock_cutting..."
        mutation_rate = mutation_rate
        population = self.random_population(population_size)

        # print population
        # while lowest > 3999:
        best_fitness = 100000
        best_geno = None
        iter = 0
        start_time = time.time()
        for iter in range(0, iteration):
            # while best_fitness>1764.0:
            # print populatio5
            newGen = []

            while len(newGen) < population_size:

                prob = random.uniform(0, 1)
                if prob < mutation_rate:

                    parent = random.choice(population)

                    child = self.mutation(parent.chromosome)
                    newGen.append(child)

                else:

                    parent1, parent2 = self.tournament_selection(population)
                    child1, child2 = self.crossover(parent1.chromosome, parent2.chromosome)
                    newGen.append(child1)
                    if child1 != child2:
                        newGen.append(child1)
            # sys.stdout.write('\r')
            # sys.stdout.write("iteration: %s || seconds: %s || mutation rate: %s" % (str(iter), time.time() - start_time, str(mutation_rate)))
            if iter % 10 == 0:
                currbest = min(population, key=lambda x: x.fitness)
                curr_cost = currbest.fitness
                if (curr_cost < best_fitness):
                    best_geno = currbest
                    best_fitness = curr_cost
            population[:] = newGen[:]
            # iter += 1

        currbest = min(population, key=lambda x: x.fitness)
        curr_cost = currbest.fitness
        if (curr_cost < best_fitness):
            best_geno = currbest
            best_fitness = curr_cost

        return best_geno, best_fitness


class GA:
    class Genotype:
        def __init__(self, stock, piece, price, chromosome, solution={}):
            self.chromosome = chromosome
            self.solution = solution
            for s in stock:
                self.solution[s] = []
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

        def calculate_fitness_FFD(self, stock, piece, price):
            cost = 0
            items = {}
            for s in stock:
                items[s] = []
            for i in xrange(0, len(self.chromosome)):
                items[self.chromosome[i]].append(piece[i])
            for key, value in items.iteritems():

                # ga_group = GA_group(piece=value, price=price[key], stock_size=key)
                # geno, fitness = ga_group.run(20, 50, 0.2)
                # cost += geno.fitness
                # phenotype = {}
                # phenotype[geno.stock_size] = []
                # for i in xrange(0, len(geno.chromosome)):
                #     pheno_bin = []
                #     for item in geno.chromosome[i]:
                #         pheno_bin.append(piece[item])
                #     phenotype[geno.stock_size].append(pheno_bin)
                # self.solution[geno.stock_size].append(phenotype[geno.stock_size])


                solution = self.FFD(key,value)
                cost += len(solution)*price[key]
                self.solution[key] = solution

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

            if random.uniform(0, 1) < 1:
                population[:] = newGen[:]
            else:
                population = population + newGen
                # print len(population)
                population.sort(key=lambda x: x.fitness)
                del population[-population_size:]

            sys.stdout.write('\r')
            sys.stdout.write("iteration: %s || seconds: %s || mutation rate: %s" % (
            str(iter), time.time() - start_time, str(mutation_rate)))
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
    geno = GA.run(iteration=50, population_size=500, mutation_rate=0.25)
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
