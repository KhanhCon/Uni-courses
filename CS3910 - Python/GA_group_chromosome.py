import random
import bisect

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

PRICE = {10: 100, 13: 130, 15: 150}
STOCK = (10, 13, 15)
PIECE = (3, 3, 3, 3, 3, 4, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10, 10, 10)
PIECE_map = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19)


# PRICE = {4300: 86, 4250: 85, 4150: 83, 3950: 79, 3800: 68, 3700: 66, 3550: 64, 3500: 63}
# STOCK = (4300, 4250, 4150, 3950, 3800, 3700, 3550, 3500)
# PIECE = [2350, 2350, 2250, 2250, 2250, 2250, 2200, 2200, 2200, 2200, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100,
#          2100, 2100, 2100, 2100, 2100, 2100, 2100, 2050, 2050, 2050, 2050, 2050, 2050, 2000, 2000, 2000, 2000, 2000,
#          2000, 2000, 2000, 2000, 2000, 2000, 1950, 1950, 1950, 1950, 1950, 1950, 1900, 1900, 1900, 1900, 1900, 1900,
#          1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850,
#          1850, 1850, 1850, 1850, 1700, 1700, 1700, 1700, 1700, 1650, 1650, 1350, 1350, 1350, 1350, 1350, 1350, 1350,
#          1350, 1350, 1300, 1300, 1300, 1250, 1250, 1250, 1250, 1250, 1250, 1200, 1200, 1200, 1200, 1200, 1200, 1200,
#          1200, 1200, 1200, 1150, 1150, 1150, 1150, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1050, 1050, 1050]
#
# PIECE_map = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125]
#


class Genotype:
    # PIECE = None
    # STOCK = None
    # PRICE = None

    def __init__(self, item=[], stock=[]):
        self.item_chromosome = item
        self.stock_chromosome = stock

    def update_stock(self, stock, piece):
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

            if point==len(stock) or (point > 0 and l <= stock[point - 1]):
                best_stock_chromosome[i] = stock[point - 1]
            else:
                best_stock_chromosome[i] = stock[point]
        self.stock_chromosome = best_stock_chromosome

    @property
    def item_chromosome(self):
        return self.item_chromosome

    @staticmethod
    def crossover(item_chromosome1, item_chromosome2, stock, piece):

        def in_list_of_list(item, lists):
            isIn = False
            for i in lists:
                if item in i:
                    isIn = True
                    break
            return isIn

        def rm_duplicates(p1, p2, items, seen):
            deleted_items = []
            deleted_groups = []
            rAnge = (range(0, p1) + range(p2, len(items)))
            # print"----"
            # print rAnge
            # print'----'
            for l in rAnge:
                acc_rm = []
                group = items[l]
                delete = False
                for i in xrange(0, len(group)):  # set(items[l]):#don't need set because lists doesn't have duplicates
                    # print i
                    if not in_list_of_list(group[i], seen):
                        acc_rm.append(i)
                    else:
                        delete = True
                if delete == True:
                    deleted_groups.append(l)
                    for index in acc_rm:
                        deleted_items.append(group[index])
            pos = 0
            deleted_groups.sort(reverse=True)
            for i in deleted_groups:
                del items[i - pos]
                # pos += 1

            return [deleted_items, items]

        child1 = []
        child2 = []
        child1[:] = item_chromosome1[:]
        child2[:] = item_chromosome2[:]
        # print(child2)
        crosspoint1 = sorted(random.sample(xrange(0, len(item_chromosome1)), 2))
        crosspoint2 = sorted(random.sample(xrange(0, len(item_chromosome2)), 2))
        insertpoint1 = random.randint(crosspoint1[0], crosspoint1[1])
        insertpoint2 = random.randint(crosspoint2[0], crosspoint2[1])
        child1[insertpoint1:insertpoint1] = item_chromosome2[crosspoint2[0]:crosspoint2[1]]
        child2[insertpoint2:insertpoint2] = item_chromosome1[crosspoint1[0]:crosspoint1[1]]
        # print crosspoint2
        # print child2
        # print "-----"
        # print item_chromosome1[crosspoint1[0]:crosspoint1[1]]
        # print crosspoint1
        # print crosspoint1
        rm_dup1 = rm_duplicates(insertpoint2, insertpoint2 + crosspoint2[1] - crosspoint2[0], child2,
                                seen=item_chromosome1[crosspoint1[0]:crosspoint1[1]])
        rm_dup2 = rm_duplicates(insertpoint1, insertpoint1 + crosspoint1[1] - crosspoint1[0], child1,
                                seen=item_chromosome2[crosspoint2[0]:crosspoint2[1]])
        child1 = rm_dup2[1]
        child2 = rm_dup1[1]

        # total = 0
        # for i in child1:
        #         total += len(i)
        # print total
        #
        # print rm_dup2[0]
        if len(rm_dup2) > 0:
            chro1 = FFD(stock, piece, rm_dup2[0])
            # print chro1
            child1 += chro1[0]

        if len(rm_dup1) > 0:
            chro2 = FFD(stock, piece, rm_dup1[0])
            # print chro1
            child1 += chro2[0]

        geno1 = Genotype(child1)
        geno1.update_stock(stock, piece)
        geno2 = Genotype(child2)
        geno2.update_stock(stock, piece)

        return geno1, geno2


    def crossover_2(item_chromosome1, item_chromosome2, stock, piece):

        def in_list_of_list(item, lists):
            isIn = False
            for i in lists:
                if item in i:
                    isIn = True
                    break
            return isIn

        def rm_duplicates(p1, items, seen):
            deleted_items = []
            deleted_groups = []
            rAnge = (range(0, p1)
            # print"----"
            # print rAnge
            # print'----'
            for l in rAnge:
                acc_rm = []
                group = items[l]
                delete = False
                for i in xrange(0, len(group)):  # set(items[l]):#don't need set because lists doesn't have duplicates
                    # print i
                    if not in_list_of_list(group[i], seen):
                        acc_rm.append(i)
                    else:
                        delete = True
                if delete == True:
                    deleted_groups.append(l)
                    for index in acc_rm:
                        deleted_items.append(group[index])
            pos = 0
            deleted_groups.sort(reverse=True)
            for i in deleted_groups:
                del items[i - pos]
                # pos += 1

            return [deleted_items, items]

        child1 = []
        child2 = []
        child1[:] = item_chromosome1[:]
        child2[:] = item_chromosome2[:]


        insertpoint1 = random.randint(0, len(item_chromosome1)-1)
        # insertpoint2 = random.randint(0, len(item_chromosome2)-1)

        child1[insertpoint1:] = item_chromosome2[insertpoint1:]
        # child2[insertpoint2:] = item_chromosome1[insertpoint2:]

        # rm_dup1 = rm_duplicates(insertpoint2, insertpoint2 + crosspoint2[1] - crosspoint2[0], child2,
        #                         seen=item_chromosome1[crosspoint1[0]:crosspoint1[1]])
        rm_dup2 = rm_duplicates(insertpoint1, insertpoint1 + crosspoint1[1] - crosspoint1[0], child1,
                                seen=item_chromosome2[crosspoint2[0]:crosspoint2[1]])
        child1 = rm_dup2[1]
        # child2 = rm_dup1[1]

        # total = 0
        # for i in child1:
        #         total += len(i)
        # print total
        #
        # print rm_dup2[0]
        if len(rm_dup2) > 0:
            chro1 = FFD(stock, piece, rm_dup2[0])
            # print chro1
            child1 += chro1[0]

        # if len(rm_dup1) > 0:
        #     chro2 = FFD(stock, piece, rm_dup1[0])
        #     # print chro1
        #     child1 += chro2[0]

        geno1 = Genotype(child1)
        geno1.update_stock(stock, piece)
        geno2 = Genotype(child2)
        geno2.update_stock(stock, piece)

        return geno1, geno2


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


def FFD(stock, piece, piece_mapping):
    def piece_sum(piece_map):
        total = 0
        for p in piece_map:
            total += piece[p]
        return total

    item_chromosome = []
    stock_chromosome = []
    # geno = Genotype()
    position = len(piece_mapping) - 1
    # for position in xrange(len(PIECE)-1,-1,-1):
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
    return item_chromosome, stock_chromosome


def random_solution(geno, stock, piece, piece_mapping):
    copy_piece_mapping = []
    copy_piece_mapping[:] = piece_mapping[:]
    random.shuffle(copy_piece_mapping)
    geno.item_chromosome, geno.stock_chromosome = FFD(stock, piece, copy_piece_mapping)
    # solution.append({"length": random_stock, "solution_pieces": solution_pieces})
    return geno


def random_population(population_size, stock, piece, piece_mapping):
    population = []
    for i in xrange(0, population_size):
        population.append(random_solution(Genotype(), stock, piece, piece_mapping))
    return population

for i in xrange(0,1000):
    chro1 = FFD(STOCK, PIECE, PIECE_map)
    chro2 = FFD(STOCK, PIECE, PIECE_map)
    #
    # # print chro2[0]
    #
    geno1 = Genotype(chro1[0], chro1[1])
    geno2 = Genotype(chro2[0], chro2[1])

    # print(geno1.item_chromosome[6])
    # print(geno1.stock_chromosome[6])
    # for i in xrange(0,15000):
    # geno1 = random_solution(Genotype(),STOCK, PIECE, PIECE_map )
    # geno2 = random_solution(Genotype(),STOCK, PIECE, PIECE_map )

    child1, child2 = Genotype.crossover(geno1.item_chromosome, geno2.item_chromosome, STOCK, PIECE)
    seen = set()
    repeated = set()
    for l in child2.item_chromosome:
      for i in set(l):
        if i in seen:
          # repeated.add(i)
          print child2.item_chromosome
          print i
          print "dup TT"
        else:
          # print"notaaaaa"
          seen.add(i)
#
#
#
# print(child1.item_chromosome)
# print(child1.stock_chromosome)
# print(len(child1.item_chromosome))
# print(len(child1.stock_chromosome))
#
# print(child2.item_chromosome)
# print(child2.stock_chromosome)
#
# print FFD(STOCK, PIECE, sorted((11, 8)))



# print Genotype.STOCK
# geno = Genotype(item=[[19], [18], [17], [16], [15], [14], [13], [12, 11], [10, 9], [8], [7, 6, 5], [4], [3, 2, 1], [0]])
# print geno.item_chromosome
# print geno.stock_chromosome
# geno.update_stock()
# print geno.stock_chromosome

# geno = Genotype()

# pop = random_population(100, STOCK, PIECE, PIECE_map)
#
# for i in pop:
#     total = 0
#     for j in i.item_chromosome:
#          for j2 in j:
#             total += j2
#     print total
#
#     print i.item_chromosome
    # print i.stock_chromosome
