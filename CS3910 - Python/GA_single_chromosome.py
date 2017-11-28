import random, time, sys


class GA:
    class Genotype:
        def __init__(self, stock, piece, price, chromosome):
            self.chromosome = chromosome
            self.fitness = self.calculate_fitness(stock, piece, price)

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
            return bins

        def calculate_fitness(self, stock, piece, price):
            cost = 0
            items = {}
            for s in stock:
                items[s] = []
            for i in xrange(0, len(self.chromosome)):
                items[self.chromosome[i]].append(piece[i])
            for key, value in items.iteritems():
                cost += len(self.FFD(key, value)) * price[key]
            return cost



        def print_solution(self, stock, piece, price):
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
                    if sum(bin) >key:
                        print "Exceed: %s:  %s"%(key,bin)
                for i in bins:
                    bin_p += len(i)
                for bin in bins:
                    for item in bin:
                        pie.append(item)
                # print "%i: %s" % (key, value)
                print "%i: %s" % (key, bins)
            print "chromosome: %s"%self.chromosome
            print "cost: %s"%self.fitness

            print "--------"

            print "Piece lengths: %s"%(sorted(list(set(pie))))

            for p in sorted(set(pie)):
                quantities.append(pie.count(p))
            print "Quantities:     %s"%quantities

            print bin_p
            print pieces


    def __init__(self, stock, piece, price):
        self.solution = None
        self.stock = stock
        self.piece = piece
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
        print "running EA_stock_cutting..."
        mutation_rate = mutation_rate
        population = self.random_population(population_size)

        for i in range(0, iteration):
            newGen = []
            while len(newGen) < population_size:

                prob = random.uniform(0, 1)
                if prob < mutation_rate:
                    index = random.randint(0, len(population) - 1)
                    newGen.append(self.scramble_mutation(population[index].chromosome))
                else:
                    parents = self.tournament_selection(population)
                    children = self.uniform_crossover([parents[0].chromosome, parents[1].chromosome])
                    newGen.append(children[0])
                    if children[0] != children[1]:
                        newGen.append(children[1])
            population[:] = newGen[:]
        best = None
        lowest = 10000
        for i in population:
            cost = i.fitness
            if cost < lowest:
                best = i
                lowest = cost
        # print_solution(stock, piece, price, best)
        best.print_solution(self.stock,self.piece,self.price)
        # print lowest
        self.solution = best
        return best


if __name__ == '__main__':
    price = {10: 100, 13: 130, 15: 150}
    stock = (10, 13, 15)
    piece = [3, 3, 3, 3, 3, 4, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10, 10, 10]

    price2 = {4300: 86, 4250: 85, 4150: 83, 3950: 79, 3800: 68, 3700: 66, 3550: 64, 3500: 63}
    stock2 = (4300, 4250, 4150, 3950, 3800, 3700, 3550, 3500)
    # PIECE = [2350, 2350, 2250, 2250, 2250, 2250, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2100, 2100, 2100, 2100, 2100, 2100, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050, 2050,
    # 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 1950,1950, 1950, 1950, 1950,  1900,1900, 1850,1850,1850,1850,1850,1850,1850,1850,1850, 1700, 1700,1700,1650,1650,1650,1650,1650,1650, 1350, 1350,1350,1350,1350,1350,1350,1350,1350,1350,1300, 1250, 1200, 1150, 1100, 1050]
    piece2 = [2350, 2350, 2250, 2250, 2250, 2250, 2200, 2200, 2200, 2200, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100,
             2100, 2100, 2100, 2100, 2100, 2100, 2100, 2050, 2050, 2050, 2050, 2050, 2050, 2000, 2000, 2000, 2000, 2000,
             2000, 2000, 2000, 2000, 2000, 2000, 1950, 1950, 1950, 1950, 1950, 1950, 1900, 1900, 1900, 1900, 1900, 1900,
             1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850,
             1850, 1850, 1850, 1850, 1700, 1700, 1700, 1700, 1700, 1650, 1650, 1350, 1350, 1350, 1350, 1350, 1350, 1350,
             1350, 1350, 1300, 1300, 1300, 1250, 1250, 1250, 1250, 1250, 1250, 1200, 1200, 1200, 1200, 1200, 1200, 1200,
             1200, 1200, 1200, 1150, 1150, 1150, 1150, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1050, 1050, 1050]

    piece2.sort(reverse=True)
    piece.sort(reverse=True)

    start_time = time.time()

    GA = GA(stock2, piece2, price2)
    GA.run(iteration=5000, population_size=200, mutation_rate=0.1)

    print("--- %s seconds ---" % (time.time() - start_time))
