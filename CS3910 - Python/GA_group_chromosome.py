import random
import bisect
import sys

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



class Genotype:
    # PIECE = None
    # STOCK = None
    # PRICE = None

    def __init__(self, item=[], stock=[]):
        self.item_chromosome = item
        self.stock_chromosome = stock
        fitness = 0

    def evaluate(self,price):
        fitness = 0
        for stock in self.stock_chromosome:
            fitness += price[stock]
        return fitness

    def update_stock(self, stock, piece,price):
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

            if point == len(stock) or (point > 0 and l <= stock[point - 1]):
                best_stock_chromosome[i] = stock[point - 1]
            else:
                best_stock_chromosome[i] = stock[point]
        self.stock_chromosome = best_stock_chromosome
        self.fitness = self.evaluate(price)



    @property
    def item_chromosome(self):
        return self.item_chromosome

    @staticmethod
    def crossover(item_chromosome1, item_chromosome2, stock, piece,price):

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

        crosspoint1 = sorted(random.sample(xrange(0, len(item_chromosome1) - 1), 2))
        crosspoint2 = sorted(random.sample(xrange(0, len(item_chromosome2) - 1), 2))
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
            chro1 = FFD(stock, piece, rm_dup2[0])
            child1 += chro1[0]

        if len(rm_dup1[0]) > 0:
            chro2 = FFD(stock, piece, rm_dup1[0])
            child2 += chro2[0]

        geno1 = Genotype(child1)
        geno1.update_stock(stock, piece,price)
        geno2 = Genotype(child2)
        geno2.update_stock(stock, piece,price)

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
    return [item_chromosome, stock_chromosome]


def random_solution(geno, stock, piece, piece_mapping,price):
    copy_piece_mapping = []
    copy_piece_mapping[:] = piece_mapping[:]
    random.shuffle(copy_piece_mapping)
    geno.item_chromosome, geno.stock_chromosome = FFD(stock, piece, copy_piece_mapping)
    geno.update_stock(stock,piece,price)
    # solution.append({"length": random_stock, "solution_pieces": solution_pieces})
    return geno


def random_population(population_size, stock, piece, piece_mapping):
    population = []
    for i in xrange(0, population_size):
        population.append(random_solution(Genotype(), stock, piece, piece_mapping))
    return population


if __name__ == '__main__':
    if True:
        geno1 = random_solution(Genotype(), piece=PIECE, piece_mapping=PIECE_map, stock=STOCK,price=PRICE)
        geno2 = random_solution(Genotype(), piece=PIECE, piece_mapping=PIECE_map, stock=STOCK,price=PRICE)
        print geno1.item_chromosome
        print geno2.item_chromosome
        child1, child2 = Genotype.crossover(geno1.item_chromosome, geno2.item_chromosome, STOCK, PIECE,PRICE)
        print "---"
        print child1.stock_chromosome
        print child1.fitness

        print "--"
        print child2.item_chromosome
        print geno2.item_chromosome
    if True:
        for i in xrange(0, 10000):
            chro1 = FFD(STOCK, PIECE, PIECE_map)
            chro2 = FFD(STOCK, PIECE, PIECE_map)

            geno1 = Genotype(chro1[0], chro1[1])
            geno2 = Genotype(chro2[0], chro2[1])

            geno1 = random_solution(Genotype(), piece=PIECE, piece_mapping=PIECE_map, stock=STOCK,price = PRICE)
            geno2 = random_solution(Genotype(), piece=PIECE, piece_mapping=PIECE_map, stock=STOCK, price = PRICE)

            child1, child2 = Genotype.crossover(geno1.item_chromosome, geno2.item_chromosome, STOCK, PIECE,PRICE)
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


