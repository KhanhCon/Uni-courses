import random

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

price = {10: 100, 13: 130, 15: 150}
stock = (10, 13, 15)
piece = (3, 3, 3, 3, 3, 4, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10, 10, 10)


class Genotype:
    PIECE = None

    def __init__(self):
        self.item_chromosome = []
        self.stock_chromosome = []

    @property
    def item_chromosome(self):
        return self.item_chromosome

    @staticmethod
    def crossover(geno1, geno2):

        def rm_duplicates(p1, p2, items, seen):
            deleted_items = []
            for l in (xrange(0, p1 + 1) + xrange(p2, len(items))):
                acc_rm = []
                group = items[l]
                delete = False
                for i in xrange(0,len(group)):  #set(items[l]):#don't need set because lists doesn't have duplicates
                    if i not in seen:
                        acc_rm.append(i)
                        seen.add(i)
                    else:
                        delete = True
                if delete:
                    for index in acc_rm:
                        deleted_items.append(group[index])
                    items.remove[l]
            return deleted_items


        child1 = []
        child2 = []
        child1[:] = geno1[:]
        child2[:] = geno2[:]
        crosspoint1 = random.sample(xrange(0, len(geno1)), 2)
        crosspoint2 = random.sample(xrange(0, len(geno2)), 2)
        insertpoint1 = random.randint(crosspoint2[0], crosspoint2[1])
        child1[insertpoint1:insertpoint1] =
        0


# First Fit Decreasing algorithm for initialization
def FFD(geno, stock, piece):
    def piece_sum(pieces):
        total = 0
        for p in pieces:
            total += piece[p]
        return total

    # geno = Genotype()
    position = len(piece) - 1
    # for position in xrange(len(piece)-1,-1,-1):
    while position >= 0:
        random_stock = random.choice(stock)
        solution_pieces = []
        while random_stock - piece_sum(solution_pieces) >= piece[position]:
            item = piece[position]
            if random_stock - piece_sum(solution_pieces) >= item:
                solution_pieces.append(position)
                position -= 1
        geno.item_chromosome.append(solution_pieces)
        geno.stock_chromosome.append(random_stock)
    return geno


geno1 = FFD(Genotype(), stock, piece)
geno2 = FFD(Genotype(), stock, piece)

print(geno1.item_chromosome[6])
print(geno1.stock_chromosome[6])


def group_crossover(parent1, parent2):
    0
