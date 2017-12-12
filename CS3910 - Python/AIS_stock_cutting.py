import random, sys, bisect, time, math
import sys, heapq, itertools
from itertools import chain


class Genotype:
    def __init__(self, fitness, item=[]):
        self.item_chromosome = item
        # self.stock_chromosome = stock_chromosome
        self.fitness = fitness
        # self.fitness = self.calculate_fitness(stock, piece, price)

    def clone(self, clone_size_factor):
        clones = []
        clone_chromosome = []
        clone_chromosome[:] = self.item_chromosome[:]
        for i in xrange(0, clone_size_factor):
            clones.append(Genotype(self.fitness, clone_chromosome))
        return clones

        # def calculate_fitness(self, stock, piece, price):
        #     def piece_sum(piece_map):
        #         total = 0
        #         for p in piece_map:
        #             total += piece[p]
        #         return total
        #
        #     best_stock_chromosome = [None] * len(self.item_chromosome)
        #     for i in xrange(0, len(best_stock_chromosome)):
        #         l = piece_sum(self.item_chromosome[i])
        #         point = (bisect.bisect(stock, l))
        #         if point == len(stock) or (point > 0 and l <= stock[point - 1]):
        #             best_stock_chromosome[i] = stock[point - 1]
        #         else:
        #             best_stock_chromosome[i] = stock[point]
        #
        #     fitness = 0
        #     for stock in best_stock_chromosome:
        #         fitness += price[stock]
        #     return fitness
        # def FF(self, piece_mapping):
        #     def piece_sum(piece_map):
        #         total = 0
        #         for p in piece_map:
        #             total += self.piece[p]
        #         return total
        #
        #     item_chromosome = []
        #     stock_chromosome = []
        #     copy_piece_map = []
        #     copy_piece_map[:] = piece_mapping[:]
        #     # copy_piece_map.sort()
        #     while len(copy_piece_map) > 0:
        #         _yield = float('-inf')
        #         best_solution = None
        #         best_stock = None
        #         for stock_size in self.stock:
        #             solution_pieces = []
        #             for piece_index in reversed(copy_piece_map):
        #                 item = self.piece[piece_index]
        #                 if stock_size - piece_sum(solution_pieces) >= item:
        #                     solution_pieces.append(piece_index)
        #             current_yield = (float(piece_sum(solution_pieces))) / float(self.price[stock_size])
        #
        #             if current_yield > _yield:
        #                 _yield = current_yield
        #                 best_solution = solution_pieces
        #                 best_stock = stock_size
        #
        #
        #         item_chromosome.append(best_solution)
        #         stock_chromosome.append(best_stock)
        #         for sol in best_solution:
        #             copy_piece_map.remove(sol)
        #
        #     return item_chromosome
        #     return [item_chromosome, stock_chromosome]
        # def mutate(self, best_fitness, mutate_constant):
        #     x = math.frexp(-mutate_constant*(self.fitness/best_fitness))*len(self.item_chromosome)
        #     numOfMutatedBins = int(round(x))
        #     starting_point = random.randint(0,len(self.item_chromosome)-1)
        #     # num_of_bins = random.randint(3, 5)
        #     to_be_delete = []
        #     mutating_pieces = []
        #     child = []
        #     child[:] = self.item_chromosome[:]
        #     for i in xrange(starting_point,starting_point + numOfMutatedBins):
        #         bin = child[i%len(child)]
        #         mutating_pieces += bin
        #         to_be_delete.append(i%len(child))
        #     to_be_delete.sort(reverse=True)
        #     for i in to_be_delete:
        #         del child[i]
        #     mutating_pieces.sort()
        #     # child += self.FF(mutating_pieces)[0]
        #     child += self.FF(mutating_pieces)
        #
        #     geno = Genotype(child)
        #     # geno.update_stock(self.stock, self.piece, self.price)
        #     return geno
        # def print_phenotype(self, piece):
        #     item_pheno = []
        #     for bin in self.item_chromosome:
        #         pheno_bin = []
        #         for item in bin:
        #             pheno_bin.append(piece[item])
        #         item_pheno.append(pheno_bin)
        #     print item_pheno
        # def print_solution(self, piece, stock):
        #     solution = {}
        #     for s in stock:
        #         solution[s] = []
        #     for i in xrange(0, len(self.item_chromosome)):
        #         pheno_bin = []
        #         for item in self.item_chromosome[i]:
        #             pheno_bin.append(piece[item])
        #         solution[self.stock_chromosome[i]].append(pheno_bin)
        #
        #     piece_test = []
        #     for key, value in solution.iteritems():
        #         piece_test.append(list(chain(*value)))
        #         for val in value:
        #             if sum(val) > key:
        #                 print "Exceed"
        #     piece_test = sorted(chain(*piece_test), reverse=False)
        #     if piece_test == piece:
        #         print "Check piece: Passed"
        #     else:
        #         print "Check piece: Failed"
        #         print piece_test
        #
        #     for key, value in solution.iteritems():
        #         print "%s: %s" % (key, value)
        # def evaluate(self, price):
        #     fitness = 0
        #     for stock in self.stock_chromosome:
        #         fitness += price[stock]
        #     return fitness
        # def update_stock(self, stock, piece, price):
        #     def piece_sum(piece_map):
        #         total = 0
        #         for p in piece_map:
        #             total += piece[p]
        #         return total
        #
        #     best_stock_chromosome = [None] * len(self.item_chromosome)
        #     for i in xrange(0, len(best_stock_chromosome)):
        #         l = piece_sum(self.item_chromosome[i])
        #         # print l
        #         point = (bisect.bisect(stock, l))
        #         # for s in sorted(stock):
        #         #     if l <= s:
        #         #         best_stock_chromosome[i] = s
        #         if point == len(stock) or (point > 0 and l <= stock[point - 1]):
        #             best_stock_chromosome[i] = stock[point - 1]
        #         else:
        #             best_stock_chromosome[i] = stock[point]
        #     self.stock_chromosome = best_stock_chromosome
        #     self.fitness = self.evaluate(price)


class AIS:
    def __init__(self, data, population_size, replacement_number, clone_size_factor, mutate_constant):
        self.stock = sorted(data["stock"])
        self.piece = sorted(data["piece"])
        self.price = data["price"]
        self.piece_map = range(0, len(data["piece"]))
        self.population_size = population_size
        self.replacement_number = replacement_number
        self.clone_size_factor = clone_size_factor
        self.mutate_constant = mutate_constant
        self.fe_count = 0

    def print_geno(self, geno):
        best_stock_chromosome = [None] * len(geno.item_chromosome)
        for i in xrange(0, len(best_stock_chromosome)):
            piece_sum = sum([self.piece[p] for p in geno.item_chromosome[i]])
            l = piece_sum
            point = (bisect.bisect(self.stock, l))
            best_stock = None
            best_price = float('inf')
            for p in xrange(point - 1, len(self.stock)):
                # if p>=len(self.stock):
                #     break
                if self.stock[p] >= l and best_price > self.price[self.stock[p]]:
                    best_price = self.price[self.stock[p]]
                    best_stock = self.stock[p]
            best_stock_chromosome[i] = best_stock
            # if point == len(self.stock) or (point > 0 and l <= self.stock[point - 1]):
            #     best_stock_chromosome[i] = self.stock[point - 1]
            # else:
            #     best_stock_chromosome[i] = self.stock[point]

        solution = {}
        for s in self.stock:
            solution[s] = []
        for i in xrange(0, len(geno.item_chromosome)):
            pheno_bin = []
            for item in geno.item_chromosome[i]:
                pheno_bin.append(self.piece[item])
            solution[best_stock_chromosome[i]].append(pheno_bin)

        piece_test = []
        exceed = False
        for key, value in solution.iteritems():
            piece_test.append(list(chain(*value)))
            for val in value:
                if sum(val) > key:
                    exceed = True
                    print "Exceed: %s: %s = %s"%(key,sum(val),val)
        if exceed:
            print "Check exceed:Failed"
        else:
            print "Check exceed:Passed"

                    # print "Exceed"
        piece_test = sorted(chain(*piece_test), reverse=False)
        if piece_test == self.piece:
            print "Check piece: Passed"
        else:
            print "Check piece: Failed"
            print piece_test
        fitness = 0
        for key, value in solution.iteritems():
            fitness += len(value) * self.price[key]
            print "%s: %s" % (key, value)
        if fitness == geno.fitness:
            print "Fitness check: Passed"
            print "Cost: %s" % fitness
        else:
            print "Fitness check: Failed - cost= %s geno.fitness = %s"% (fitness,geno.fitness)
        # print "cost: %s" % fitness

    def calculate_fitness(self, item_chromosome):

        best_stock_chromosome = [None] * len(item_chromosome)
        for i in xrange(0, len(best_stock_chromosome)):
            piece_sum = sum([self.piece[p] for p in item_chromosome[i]])
            l = piece_sum
            point = (bisect.bisect(self.stock, l))
            best_stock = None
            best_price = float('inf')
            for p in xrange(point - 1, len(self.stock)):
                # if p>=len(self.stock):
                #     break
                if self.stock[p] >= l and best_price > self.price[self.stock[p]]:
                    best_price = self.price[self.stock[p]]
                    best_stock = self.stock[p]
            best_stock_chromosome[i] = best_stock
            # if point == len(self.stock) or (point > 0 and l <= self.stock[point - 1]):
            #     best_stock_chromosome[i] = self.stock[point - 1]
            # else:
            #     best_stock_chromosome[i] = self.stock[point]

        fitness = 0
        for stock in best_stock_chromosome:
            fitness += self.price[stock]
        self.fe_count += 1
        return fitness

    # # item_chromosome, stock, piece, price
    # def mutation(self,item_chromosome, numOfMutatedBins):
    #     starting_point = random.randint(0,len(item_chromosome)-1)
    #     num_of_bins = random.randint(3, 5)
    #     to_be_delete = []
    #     mutating_pieces = []
    #     child = []
    #     child[:] = item_chromosome[:]
    #     for i in xrange(starting_point,starting_point + num_of_bins):
    #         bin = child[i%len(child)]
    #         mutating_pieces += bin
    #         to_be_delete.append(i%len(child))
    #     to_be_delete.sort(reverse=True)
    #     for i in to_be_delete:
    #         del child[i]
    #     mutating_pieces.sort()
    #     child += self.FF(mutating_pieces)[0]
    #
    #     geno = Genotype(child)
    #     # geno.update_stock(self.stock, self.piece, self.price)
    #     return geno
    def FF(self, piece_mapping):
        def piece_sum(piece_map):
            total = 0
            for p in piece_map:
                total += self.piece[p]
            return total

        item_chromosome = []
        stock_chromosome = []
        copy_piece_map = []
        copy_piece_map[:] = piece_mapping[:]
        # copy_piece_map.sort()
        while len(copy_piece_map) > 0:
            _yield = float('-inf')
            best_solution = None
            best_stock = None
            for stock_size in self.stock:
                solution_pieces = []
                for piece_index in reversed(copy_piece_map):
                    item = self.piece[piece_index]
                    if stock_size - piece_sum(solution_pieces) >= item:
                        solution_pieces.append(piece_index)
                # current_yield = float((stock - piece_sum(solution_pieces))/float(stock))*float(self.price[stock])
                current_yield = (float(piece_sum(solution_pieces))) / float(self.price[stock_size])
                # current_yield = float(stock - piece_sum(solution_pieces))*float(self.price[stock])

                if current_yield > _yield:
                    # print PRICE2[stock]
                    _yield = current_yield
                    # _yield = piece_sum(solution_pieces) / stock
                    best_solution = solution_pieces
                    best_stock = stock_size
                    # elif(float(piece_sum(solution_pieces)) / stock == _yield):
                    #     if random.randint(1,5)==2:
                    #         _yield = piece_sum(solution_pieces) / stock
                    #         best_solution = solution_pieces
                    #         best_stock = stock

            item_chromosome.append(best_solution)
            stock_chromosome.append(best_stock)
            for sol in best_solution:
                copy_piece_map.remove(sol)

        return item_chromosome

    def mutate(self, geno, best_fitness):
        # if geno.fitness>4500:
        #     print "LARGE"
        x = math.exp(-self.mutate_constant * (float(best_fitness) / geno.fitness))
        # x = (1/self.mutate_constant)*(math.exp(float(best_fitness)/geno.fitness))
        x = x * len(geno.item_chromosome)
        numOfMutatedBins = int(round(x))
        # print numOfMutatedBins
        starting_point = random.randint(0, len(geno.item_chromosome) - 1)
        # num_of_bins = random.randint(3, 5)
        tobe_deleted_group = []
        mutating_pieces = []
        child = []
        child[:] = geno.item_chromosome[:]
        for i in xrange(starting_point, starting_point + numOfMutatedBins):
            bin = child[i % len(child)]
            mutating_pieces += bin
            tobe_deleted_group.append(i % len(child))
        tobe_deleted_group.sort(reverse=True)
        for i in tobe_deleted_group:
            del child[i]
        mutating_pieces.sort()
        # child += self.FF(mutating_pieces)[0]
        child += self.FF(mutating_pieces)
        fitness = self.calculate_fitness(child)
        geno = Genotype(fitness, child)
        # geno.update_stock(self.stock, self.piece, self.price)
        # print "mutate"
        return geno

    def random_chromosome(self, piece_mapping):
        def piece_sum(piece_map):
            total = 0
            for p in piece_map:
                total += self.piece[p]
            return total

        item_chromosome = []
        stock_chromosome = []
        position = len(piece_mapping) - 1
        while position >= 0:
            # for position in piece_mapping:
            random_stock = random.choice(self.stock)
            solution_pieces = []
            while random_stock - piece_sum(solution_pieces) >= self.piece[piece_mapping[position]] and position >= 0:
                item = self.piece[piece_mapping[position]]
                if random_stock - piece_sum(solution_pieces) >= item:
                    solution_pieces.append(piece_mapping[position])
                    position -= 1
            item_chromosome.append(solution_pieces)
            # stock_chromosome.append(random_stock)
        return item_chromosome

    def random_solution(self):
        copy_piece_mapping = []
        copy_piece_mapping[:] = self.piece_map[:]
        random.shuffle(copy_piece_mapping)
        item_chromosome = self.FF(copy_piece_mapping)
        fitness = self.calculate_fitness(item_chromosome)
        geno = Genotype(fitness, item_chromosome)

        return geno

    def random_population(self):

        population = [self.random_solution() for _ in xrange(0, self.population_size)]
        population.sort(key=lambda x: x.fitness, reverse=True)

        return population

    def select(self, population):
        return list(reversed(heapq.nsmallest(self.population_size, population, key=lambda x: x.fitness)))

    def replace_d(self, population,function_evaluation):
        if self.replacement_number == 0 or self.fe_count - function_evaluation <= 0:
            return population

        replacement_number = self.replacement_number if self.fe_count - function_evaluation > self.replacement_number else self.fe_count - function_evaluation
        population[0:replacement_number] = [self.random_solution() for _ in xrange(0, self.clone_size_factor)]
        population.sort(key=lambda x: x.fitness, reverse=True)
        return population

    def run(self, function_evaluation):
        print("Running AIS...")
        population = self.random_population()
        best_fitness = population[-1].fitness
        count = 0
        # for i in xrange(0,function_evaluation):
        while self.fe_count < function_evaluation:
        # for _ in xrange(0, function_evaluation):
            clone_pool = []
            for _ in xrange(0, self.clone_size_factor):
                for geno in population:
                    if self.fe_count >= function_evaluation:
                        return sorted(population,key=lambda x: x.fitness, reverse=True)[-1]
                    clone_pool.append(self.mutate(geno, best_fitness))
                # clone_pool += [self.mutate(geno, best_fitness) for geno in population]
            population += clone_pool

            # population += [self.mutate(geno, best_fitness) for geno in population]*self.clone_size_factor
            # print len(clone_pool)
            # for geno in population:
            #     mutated_clones = []
            #     for clone in geno.clone(self.clone_size_factor):
            #         mutated_clones.append(self.mutate(clone, best_fitness))
            #     clone_pool += mutated_clones
            # population = population + clone_pool
            # print len(population)

            population = self.select(population)
            population = self.replace_d(population,function_evaluation)
            best_fitness = population[-1].fitness
            print best_fitness
            if best_fitness > population[-1].fitness:
                count = 0
            else:
                count += 1
            if count > 100:
                break
            if best_fitness < population[-1].fitness:
                print "WRONG"

        return population[-1]
        self.print_geno(population[-1])
        print population[-1].fitness
        print best_fitness


if __name__ == '__main__':
    PRICE1 = {10: 100, 13: 130, 15: 150}
    STOCK1 = (10, 13, 15)
    PIECE1 = [3, 3, 3, 3, 3, 4, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10, 10, 10]

    data1 = {
        "price": PRICE1,
        "stock": STOCK1,
        "piece": PIECE1,
    }

    PRICE2 = {4300: 86, 4250: 85, 4150: 83, 3950: 79, 3800: 68, 3700: 66, 3550: 64, 3500: 63}
    STOCK2 = (3500, 3550, 3700, 3800, 3950, 4150, 4250, 4300)
    PIECE2 = [1050, 1050, 1050, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1150, 1150, 1150, 1150, 1200, 1200,
              1200,
              1200, 1200, 1200, 1200, 1200, 1200, 1200, 1250, 1250, 1250, 1250, 1250, 1250, 1300, 1300, 1300, 1350,
              1350,
              1350, 1350, 1350, 1350, 1350, 1350, 1350, 1650, 1650, 1700, 1700, 1700, 1700, 1700, 1850, 1850, 1850,
              1850,
              1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900,
              1900,
              1900, 1900, 1900, 1900, 1900, 1900, 1950, 1950, 1950, 1950, 1950, 1950, 2000, 2000, 2000, 2000, 2000,
              2000,
              2000, 2000, 2000, 2000, 2000, 2050, 2050, 2050, 2050, 2050, 2050, 2100, 2100, 2100, 2100, 2100, 2100,
              2100,
              2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2200, 2200, 2200, 2200, 2250, 2250, 2250, 2250, 2350,
              2350]

    data2 = {
        "price": PRICE2,
        "stock": STOCK2,
        "piece": PIECE2,

    }

    STOCK3 = (100, 105, 110, 115, 120)
    PRICE3 = {120: 12, 115: 11.5, 110: 11, 105: 10.5, 100: 10}
    PIECE3 = [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
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

    data3 = {
        "price": PRICE3,
        "stock": STOCK3,
        "piece": PIECE3,
    }

    start_time = time.time()
    ais = AIS(data3, replacement_number=35, population_size=50, clone_size_factor=4, mutate_constant=1.0)
    geno = ais.run(function_evaluation=500)
    total_time = time.time() - start_time
    ais.print_geno(geno)
    print("---GA runtime: %s seconds --- \n" % (total_time))
    print ais.fe_count



    # pop = ais.random_population()
    # # print(dir(pop))
    # for i in pop:
    #     print i.fitness
    # print "---"
    # replace = ais.replace_d(pop)
    # for i in replace:
    #     print i.fitness

    geno = ais.random_solution()
    # l=[ais.mutate(geno,1765)]*10
    # for i in l:
    #     # print i.fitness
    #     0
    l = []
    for _ in itertools.repeat(None, 5):
        l.append(ais.mutate(geno, 1765))
    for i in l:
        # print i.fitness
        0
    l2 = []
    for _ in itertools.repeat(None, 2):
        l2 += [ais.mutate(geno, 1765) for geno in l]

        # for i in l2:
        #     print i.fitness
        # print ais.mutate(geno, 1765).fitness
        # print ais.mutate(geno, 1765).fitness
        # print ais.mutate(geno, 1765).fitness
    # pop = ais.random_population()
    # for i in pop:
    #     print i.fitness
    # print "----"
    # clone_pool = []
    # for _ in xrange(0, 3):
    #     clone_pool += [ais.mutate(geno, pop[-1].fitness) for geno in pop]
    # clone_pool = [ais.mutate(geno, pop[-1].fitness) for geno in pop]*3
    # pop += clone_pool
    # for i in pop:
    #     print i.fitness