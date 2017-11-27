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

    def __init__(self,item=[],stock=[]):
        self.item_chromosome = item
        self.stock_chromosome = stock

    @property
    def item_chromosome(self):
        return self.item_chromosome

    @staticmethod
    def crossover(geno1, geno2):

        def in_list_of_list(item,lists):

            isIn = False

            for i in lists:
                if item in i:
                    isIn = True
                    break
            return isIn



        def rm_duplicates(p1, p2, items, seen):
            deleted_items = []
            deleted_groups = []
            # print "ssss"
            # print seen
            for l in (range(0, p1) + range(p2, len(items))):
                acc_rm = []
                group = items[l]
                delete = False
                for i in xrange(0, len(group)):  # set(items[l]):#don't need set because lists doesn't have duplicates
                    # print i
                    if not in_list_of_list(group[i],seen):

                        acc_rm.append(i)
                        # seen.add(i)
                    else:
                        # print "in"
                        delete = True
                if delete==True:
                    # print acc_rm
                    deleted_groups.append(l)
                    for index in acc_rm:
                        deleted_items.append(group[index])

                        # print 's'
                    # print("ssss")
                    # print group
                    # del items[l]
                    # l -= 1
            # print 'ssss'
            # print deleted_groups
            pos = 0
            for i in deleted_groups:
                del items[i-pos]
                pos += 1


            return [deleted_items,items]
        # print geno1
        child1 = []
        child2 = []
        child1[:] = geno1[:]
        child2[:] = geno2[:]
        print(child2)
        # print child2
        crosspoint1 = sorted(random.sample(xrange(0, len(geno1)), 2))
        crosspoint2 = sorted(random.sample(xrange(0, len(geno2)), 2))
        insertpoint2 = random.randint(crosspoint2[0], crosspoint2[1])
        child2[insertpoint2:insertpoint2] = geno1[crosspoint1[0]:crosspoint1[1]]
        print child2
        print "-----"
        # print geno1
        print geno1[crosspoint1[0]:crosspoint1[1]]
        print crosspoint1
        # print crosspoint1
        rm_dup = rm_duplicates(insertpoint2, insertpoint2+crosspoint1[1]-crosspoint1[0], child2, seen=geno1[crosspoint1[0]:crosspoint1[1]])
        child2 = rm_dup[1]
        total = 0
        for i in child2:
            for i2 in i:
                total += 1
        print total
        return child2


# First Fit Decreasing algorithm for initialization
def FFD(stock, piece):
    def piece_sum(pieces):
        total = 0
        for p in pieces:
            total += piece[p]
        return total

    item_chromosome = []
    stock_chromosome = []
    # geno = Genotype()
    position = len(piece) - 1
    # for position in xrange(len(piece)-1,-1,-1):
    while position >= 0:
        random_stock = random.choice(stock)
        solution_pieces = []
        while random_stock - piece_sum(solution_pieces) >= piece[position] and position >=0:
            item = piece[position]
            if random_stock - piece_sum(solution_pieces) >= item:
                solution_pieces.append(position)
                position -= 1
        item_chromosome.append(solution_pieces)
        stock_chromosome.append(random_stock)
    return [item_chromosome,stock_chromosome]


chro1 = FFD(stock, piece)
chro2 = FFD(stock, piece)

print chro1

geno1 = Genotype(chro1[0],chro1[1])
geno2 = Genotype(chro2[0],chro2[1])

# print(geno1.item_chromosome[6])
# print(geno1.stock_chromosome[6])

print(Genotype.crossover(geno1.item_chromosome, geno2.item_chromosome))


def group_crossover(parent1, parent2):
    0


def in_list_of_list(item, lists):
    isIn = False

    for i in lists:
        if item in i:
            isIn = True
            break
    return isIn

# if(not in_list_of_list(0,[[18], [17], [16], [15], [14], [13], [12], [11], [10], [9], [8, 7, 6]])):
#     print "s"