import random, sys, bisect, time
import sys, heapq
from itertools import chain

# class StockSizeChromosome:
#     def __init__(self):
#         self.chromosome = []
#
#     0
#
# class ItemChromosome:
#     def __init__(self):
#         self.chromosome = [None]*
#     0

PRICE1 = {10: 100, 13: 130, 15: 150}
STOCK1 = (10, 13, 15)
PIECE1 = [3, 3, 3, 3, 3, 4, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10, 10, 10]
PIECE_map1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

data1 = {
    "price": PRICE1,
    "stock": STOCK1,
    "piece": PIECE1,
    "piece_map" : PIECE_map1
}



PRICE2 = {4300: 86, 4250: 85, 4150: 83, 3950: 79, 3800: 68, 3700: 66, 3550: 64, 3500: 63}
STOCK2 = (3500, 3550, 3700, 3800, 3950, 4150, 4250, 4300)

PIECE2 = [1050, 1050, 1050, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1150, 1150, 1150, 1150, 1200, 1200, 1200,
          1200, 1200, 1200, 1200, 1200, 1200, 1200, 1250, 1250, 1250, 1250, 1250, 1250, 1300, 1300, 1300, 1350, 1350,
          1350, 1350, 1350, 1350, 1350, 1350, 1350, 1650, 1650, 1700, 1700, 1700, 1700, 1700, 1850, 1850, 1850, 1850,
          1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900,
          1900, 1900, 1900, 1900, 1900, 1900, 1950, 1950, 1950, 1950, 1950, 1950, 2000, 2000, 2000, 2000, 2000, 2000,
          2000, 2000, 2000, 2000, 2000, 2050, 2050, 2050, 2050, 2050, 2050, 2100, 2100, 2100, 2100, 2100, 2100, 2100,
          2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2200, 2200, 2200, 2200, 2250, 2250, 2250, 2250, 2350, 2350]
PIECE_map2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
              29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
              55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
              81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105,
              106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125]

data2 = {
    "price": PRICE2,
    "stock": STOCK2,
    "piece": PIECE2,
    "piece_map" : PIECE_map2
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
PIECE_map3 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
              29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
              55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
              81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105,
              106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126,
              127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147,
              148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
              169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189,
              190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210,
              211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231,
              232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252,
              253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273,
              274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294,
              295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315,
              316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336,
              337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357,
              358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378,
              379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394]

data3 = {
    "price": PRICE3,
    "stock": STOCK3,
    "piece": PIECE3,
    "piece_map" : PIECE_map3
}


class Genotype:
    # PIECE = None
    # STOCK = None
    # PRICE = None

    def __init__(self, item=[], stock=[]):
        self.item_chromosome = item
        self.stock_chromosome = stock
        self.fitness = 0

    def print_phenotype(self, piece):
        item_pheno = []
        for bin in self.item_chromosome:
            pheno_bin = []
            for item in bin:
                pheno_bin.append(piece[item])
            item_pheno.append(pheno_bin)
        print item_pheno

    def print_solution(self, piece, stock):
        solution = {}
        for s in stock:
            solution[s] = []
        for i in xrange(0, len(self.item_chromosome)):
            pheno_bin = []
            for item in self.item_chromosome[i]:
                pheno_bin.append(piece[item])
            solution[self.stock_chromosome[i]].append(pheno_bin)

        piece_test = []
        for key, value in solution.iteritems():
            piece_test.append(list(chain(*value)))
            for val in value:
                if sum(val) > key:
                    print "Exceed"
        piece_test = sorted(chain(*piece_test), reverse=False)
        if piece_test == piece:
            print "Check piece: Passed"
        else:
            print "Check piece: Failed"
            print piece_test

        for key, value in solution.iteritems():
            print "%s: %s" % (key, value)

    def evaluate(self, price):
        fitness = 0
        for stock in self.stock_chromosome:
            fitness += price[stock]
        return fitness

    def update_stock(self, stock, piece, price):
        def piece_sum(piece_map):
            total = 0
            for p in piece_map:
                total += piece[p]
            return total

        best_stock_chromosome = [None] * len(self.item_chromosome)
        for i in xrange(0, len(best_stock_chromosome)):
            l = piece_sum(self.item_chromosome[i])
            # print l
            point = (bisect.bisect(stock, l))
            # for s in sorted(stock):
            #     if l <= s:
            #         best_stock_chromosome[i] = s
            if point == len(stock) or (point > 0 and l <= stock[point - 1]):
                best_stock_chromosome[i] = stock[point - 1]
            else:
                best_stock_chromosome[i] = stock[point]
        self.stock_chromosome = best_stock_chromosome
        self.fitness = self.evaluate(price)

    @property
    def item_chromosome(self):
        return self.item_chromosome




# First Fit Decreasing algorithm for initialization
# def FFD(stock, piece, piece_mapping):
#     def piece_sum(pieces):
#         total = 0
#         for p in pieces:
#             total += piece[p]
#         return total
#
#     item_chromosome = []
#     stock_chromosome = []
#     # geno = Genotype()
#     position = len(piece) - 1
#     # for position in xrange(len(PIECE)-1,-1,-1):
#     while position >= 0:
#         random_stock = random.choice(stock)
#         solution_pieces = []
#         while random_stock - piece_sum(solution_pieces) >= piece[position] and position >= 0:
#             item = piece[position]
#             if random_stock - piece_sum(solution_pieces) >= item:
#                 solution_pieces.append(position)
#                 position -= 1
#         item_chromosome.append(solution_pieces)
#         stock_chromosome.append(random_stock)
#     return [item_chromosome, stock_chromosome]

class GA:

    def __init__(self,data):
        self.stock = data["stock"]
        self.piece = data["piece"]
        self.price = data["price"]
        # self.piece_map = data["piece_map"]
        self.piece_map = range(0,len(data["piece"]))



    # item_chromosome, stock, piece, price
    def mutation(self,item_chromosome):
        num_of_bins = random.randint(3, 5)
        mutating_pieces = []
        child = []
        child[:] = item_chromosome[:]
        for i in xrange(0, num_of_bins):
            bin = random.choice(child)
            mutating_pieces += bin
            child.remove(bin)
        mutating_pieces.sort()
        child += self.FFD(mutating_pieces)[0]

        geno = Genotype(child)
        geno.update_stock(self.stock, self.piece, self.price)
        return geno

    # @staticmethod
    def crossover(self,item_chromosome1, item_chromosome2):

        def in_list_of_list(item, lists):
            isIn = False
            for i in lists:
                if item in i:
                    isIn = True
                    break
            return isIn

        def rm_duplicates(items, seen):

            """

            :type seen: list
            """
            deleted_items = []
            deleted_groups = []

            for l in xrange(0, len(items)):
                acc_rm = []
                group = items[l]
                delete = False
                for item in xrange(0,len(group)):  # set(items[l]):#don't need set because lists doesn't have duplicates
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

        child1 = []
        child2 = []
        child1[:] = item_chromosome1[:]
        child2[:] = item_chromosome2[:]

        try:
            crosspoint1 = sorted(random.sample(xrange(0, len(item_chromosome1) - 1), 2))
            crosspoint2 = sorted(random.sample(xrange(0, len(item_chromosome2) - 1), 2))
        except ValueError:
            print item_chromosome1
            print item_chromosome2
        # insertpoint1 = random.randint(crosspoint1[0], crosspoint1[1])
        # insertpoint2 = random.randint(crosspoint2[0], crosspoint2[1])

        # child2[insertpoint2:insertpoint2] = item_chromosome1[crosspoint1[0]:crosspoint1[1]]

        rm_dup1 = rm_duplicates(child2, seen=item_chromosome1[crosspoint1[0]:crosspoint1[1]])
        rm_dup2 = rm_duplicates(child1, seen=item_chromosome2[crosspoint2[0]:crosspoint2[1]])

        child1 = rm_dup2[1]
        child2 = rm_dup1[1]

        # insertpoint1 = random.randint(0, len(child1)-1)
        # child1[insertpoint1:insertpoint1] = item_chromosome2[crosspoint2[0]:crosspoint2[1]]

        if len(rm_dup2[0]) > 0:
            rm_dup2[0].sort()
            chro1 = self.FFD(rm_dup2[0])
            child1 += chro1[0]

        if len(rm_dup1[0]) > 0:
            rm_dup1[0].sort()
            chro2 = self.FFD(rm_dup1[0])
            child2 += chro2[0]

        geno1 = Genotype(child1)
        geno1.update_stock(self.stock, self.piece, self.price)
        geno2 = Genotype(child2)
        geno2.update_stock(self.stock, self.piece, self.price)

        return geno1, geno2

    def FFD1(stock, piece, piece_mapping):
        def piece_sum(piece_map):
            total = 0
            for p in piece_map:
                total += piece[p]
            return total

        item_chromosome = []
        stock_chromosome = []
        position = len(piece_mapping) - 1
        while position >= 0:
            # for position in piece_mapping:
            random_stock = random.choice(stock)
            solution_pieces = []
            while random_stock - piece_sum(solution_pieces) >= piece[piece_mapping[position]] and position >= 0:
                item = piece[piece_mapping[position]]
                if random_stock - piece_sum(solution_pieces) >= item:
                    solution_pieces.append(piece_mapping[position])
                    position -= 1
            item_chromosome.append(solution_pieces)
            stock_chromosome.append(random_stock)
        return [item_chromosome, stock_chromosome]


    def FFD1(stock, piece, piece_mapping):
        def piece_sum(piece_map):
            total = 0
            for p in piece_map:
                total += piece[p]
            return total

        item_chromosome = []
        stock_chromosome = []
        # geno = Genotype()
        position = len(piece_mapping) - 1
        # copy_piece = []
        # copy_piece[:] = piece[:]
        used = 0
        # for position in xrange(len(PIECE)-1,-1,-1):   piece[piece_mapping[position]]
        while position >= 0:
            # for position in piece_mapping:
            random_stock = random.choice(stock)
            solution_pieces = []
            while random_stock - piece_sum(solution_pieces) >= piece[piece_mapping[position]] and position >= 0:
                item = piece[piece_mapping[position]]
                if random_stock - piece_sum(solution_pieces) >= item:
                    solution_pieces.append(piece_mapping[position])
                    # del copy_piece[position-used]
                    used += 1
                    position -= 1
            item_chromosome.append(solution_pieces)
            stock_chromosome.append(random_stock)
        return [item_chromosome, stock_chromosome]

    # , stock, piece, piece_mapping
    def FFD(self,piece_mapping):
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
                current_yield = (float(piece_sum(solution_pieces)))/float(self.price[stock_size])
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

        return [item_chromosome, stock_chromosome]


    def FF(self,stock, piece, piece_mapping):
        def piece_sum(piece_map):
            total = 0
            for p in piece_map:
                total += piece[p]
            return total

        item_chromosome = []
        stock_chromosome = []
        copy_piece_map = []
        copy_piece_map[:] = piece_mapping[:]
        # copy_piece_map.sort()
        while len(copy_piece_map) > 0:
            _yield = 0
            best_solution = None
            best_stock = None
            for stock_size in stock:
                solution_pieces = []
                for piece_index in reversed(copy_piece_map):
                    item = piece[piece_index]
                    if stock_size - piece_sum(solution_pieces) >= item:
                        solution_pieces.append(piece_index)

                if float(piece_sum(solution_pieces)) / stock_size > _yield:
                    _yield = piece_sum(solution_pieces) / stock_size
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

        return [item_chromosome, stock_chromosome]


    def random_solution(self,geno,piece_mapping):
        copy_piece_mapping = []
        copy_piece_mapping[:] = piece_mapping[:]
        random.shuffle(copy_piece_mapping)
        geno.item_chromosome, geno.stock_chromosome = self.FFD(copy_piece_mapping)
        geno.update_stock(self.stock, self.piece, self.price)
        # solution.append({"length": random_stock, "solution_pieces": solution_pieces})
        return geno


    def random_population(self,population_size, stock, piece, piece_mapping, price):
        population = []
        for i in xrange(0, population_size):
            population.append(self.random_solution(Genotype(),piece_mapping))
        return population


    def tournament_selection(self,geno_population):
        tournament_population_size = random.randint(15, 30)
        tournament_population = random.sample(geno_population, tournament_population_size)

        # m1, m2 = float('inf'), float('inf')
        # min1, min2 = None, None
        # for x in tournament_population:
        #     x_fitness = x.fitness
        #     if x_fitness <= m1:
        #         min1, min2 = x, min1
        #         m1, m2 = x_fitness, m1
        #     elif x_fitness < m2:
        #         min2 = x
        #         m2 = x_fitness

        min1, min2 = heapq.nsmallest(2,tournament_population, key=lambda x:x.fitness)
        return min1, min2

    # , stock, piece, price, piece_map,
    def run(self, iteration, population_size=50, mutation_rate=0.00):
        print "running EA_stock_cutting..."
        mutation_rate = mutation_rate
        population = self.random_population(population_size, self.stock, self.piece, self.piece_map, self.price)

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
                # while lowest > 3999:
                # for i in xrange(0,population_size):
                prob = random.uniform(0, 1)
                if prob < mutation_rate:

                    parent = random.choice(population)

                    child = self.mutation(parent.item_chromosome)
                    newGen.append(child)
                    # index = random.randint(0, len(population) - 1)
                    # newGen.append(scramble_mutation(population[index], stock))
                else:
                    # print population
                    parent1, parent2 = self.tournament_selection(population)
                    # print parents
                    # population.remove(parents[0])
                    # if parents[1] in population:
                    #     population.remove(parents[1])
                    # print parents
                # [57,56,22,13,18]
                    child1, child2 = self.crossover(parent1.item_chromosome, parent2.item_chromosome)
                    newGen.append(child1)
                    if child1 != child2:
                        newGen.append(child1)
            sys.stdout.write('\r')
            sys.stdout.write("iteration: %s || seconds: %s || mutation rate: %s" % (str(iter), time.time() - start_time, str(mutation_rate)))
            if iter % 10 == 0:
                currbest = min(population,key=lambda x:x.fitness)
                curr_cost = currbest.fitness
                if (curr_cost < best_fitness):
                    best_geno = currbest
                    best_fitness = curr_cost
            population[:] = newGen[:]
            iter += 1
        # best = []
        # lowest = 10000
        # for Geno in population:
        #
        #     cost = Geno.fitness
        #     if cost < lowest:
        #         best = Geno
        #         lowest = cost
        # best = min(population,key=lambda x:x.fitness)
        # lowest = best.fitness
        currbest = min(population, key=lambda x: x.fitness)
        curr_cost = currbest.fitness
        if (curr_cost < best_fitness):
            best_geno = currbest
            best_fitness = curr_cost
        # print
        # print evaluate(STOCK, PIECE, PRICE, best)
        # best_geno.print_solution(PIECE2, STOCK2)
        # print best_fitness
        return best_geno, best_fitness
        # return best, lowest


if __name__ == '__main__':
    if False:
        geno1 = random_solution(Genotype(), piece=PIECE, piece_mapping=PIECE_map, stock=STOCK, price=PRICE)
        geno2 = random_solution(Genotype(), piece=PIECE, piece_mapping=PIECE_map, stock=STOCK, price=PRICE)
        print geno1.item_chromosome
        print geno2.item_chromosome
        child1, child2 = Genotype.crossover(geno1.item_chromosome, geno2.item_chromosome, STOCK, PIECE, PRICE)
        print "---"
        print child1.stock_chromosome
        print child1.fitness

        print "--"
        print child2.item_chromosome
        print geno2.item_chromosome
    if False:
        for i in xrange(0, 10000):
            chro1 = FFD(STOCK, PIECE, PIECE_map)
            chro2 = FFD(STOCK, PIECE, PIECE_map)

            geno1 = Genotype(chro1[0], chro1[1])
            geno2 = Genotype(chro2[0], chro2[1])

            geno1 = random_solution(Genotype(), piece=PIECE, piece_mapping=PIECE_map, stock=STOCK, price=PRICE)
            geno2 = random_solution(Genotype(), piece=PIECE, piece_mapping=PIECE_map, stock=STOCK, price=PRICE)

            child1, child2 = Genotype.crossover(geno1.item_chromosome, geno2.item_chromosome, STOCK, PIECE, PRICE)
            total1 = 0
            for i in child1.item_chromosome:
                total1 += len(i)
            if total1 != 20:
                print "@@"

            saw1 = set()
            for l in child1.item_chromosome:
                for i in set(l):
                    if i in saw1:
                        print "dup TT"
                        sys.exit()
                    else:
                        saw1.add(i)
            saw2 = set()
            for l in child2.item_chromosome:
                for i in set(l):
                    if i in saw2:
                        print "dup TT"
                        sys.exit()
                    else:
                        saw2.add(i)
            total2 = 0

            for i in child2.item_chromosome:
                total2 += len(i)
            if total2 != 20:
                print "@@"
    # start
    ga = GA(data2)
    geno, fitness = ga.run(iteration=20, population_size=300, mutation_rate=0.3)
    geno.print_solution(ga.piece, ga.stock)
    print fitness
    # print FFD(STOCK,PIECE,PIECE_map)
