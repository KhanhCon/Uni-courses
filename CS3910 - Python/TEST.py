import random, bisect
from itertools import chain

ebins = [[3, 3, 3], [6, 2, 1, ], [5, 2], [4, 3], [7, 2], [5, 4]]

testbin = [[3, 3, 3], [2, 6, 1, ], [7, 2], [5, 4]]

# 5/10  10
#
# 10/20 30
# saved here because it has better performance
def free(bins):
    m1, m2 = float('inf'), float('inf')
    min1, min2 = None, None
    for x in bins:
        x_fitness = sum(x)
        if x_fitness <= m1:
            min1, min2 = x, min1
            m1, m2 = x_fitness, m1
        elif x_fitness < m2:
            min2 = x
            m2 = x_fitness
    return min1 + min2


def replace(free_items, bins, bin_capacity):
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


def replace2(free_items, bins, bin_capacity):
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
                    if bre: break
                if bre: break
            if bre: break
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
                        improve21 = free_items[i1] - bin[b2] - bin[b1]
                        if (bin_capacity - sum(bin) >= improve21 and improve21 > 0):
                            free_items[i1], bin[b1], = bin[b1], free_items[i1]
                            free_items.append(bin[b2])
                            del bin[b2]
                            free_items.sort(reverse=True)
                            bre = True
                            break
                    if bre: break
                if bre: break
            if bre: break
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
                        improve11 = free_items[i1] - bin[b1]
                        if (bin_capacity - sum(bin) >= improve11 and improve11 > 0):
                            free_items[i1], bin[b1], = bin[b1], free_items[i1],
                            free_items.sort(reverse=True)
                            bre = True
                            break
                    if bre: break
                if bre: break
            if bre: break


def lsearch(bins, num_of_free_bin, bin_capacity=10):
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

    bins.sort(
        key=lambda x: (sum(x), x[0], x[1] if len(x) > 1 else 0, x[2] if len(x) > 2 else 0, x[3] if len(x) > 3 else 0),
        reverse=True)
    original_len = len(bins)
    print "......"
    print bins
    print len(bins)
    free_items = sorted(chain(*bins[-num_of_free_bin:]), reverse=True)
    del bins[-num_of_free_bin:]

    replace2(free_items, bins, bin_capacity)

    free_items = sorted(free_items, reverse=True)
    # bins.append(FFD(bin_capacity,free_items))
    for bin in FFD(bin_capacity, free_items):
        if bin:
            bins.append(bin)

    print bins
    print len(bins)
    print "-----"
    improved_len = len(bins)
    if improved_len < original_len:
        return lsearch(bins, num_of_free_bin, bin_capacity)
    else:
        return bins


# lsearch([[67, 53], [67, 53], [67, 51], [66, 50], [63, 57], [63, 57], [63, 57], [63, 57], [63, 57], [63, 57], [63, 56], [63, 56], [61, 59], [49, 49, 22], [49, 49, 22], [48, 47, 25], [47, 46, 27], [46, 44, 30], [44, 38, 38], [33, 33, 33, 21], [33, 33, 33, 21], [32, 32, 32, 24], [32, 32, 32, 24], [32, 31, 31, 25], [31, 31, 29, 29], [27, 24, 22, 21, 21]], 5, 120)


def BFD(stock_size, items):
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


# print BFD(10,[10,10,10, 7, 3, 7, 3])

STOCK = (10, 13, 15)
PIECE = (3, 3, 3, 3, 3, 4, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10, 10, 10)
PIECE_map = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


def FFD(stock, piece, piece_mapping):
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
        # random_stock = random.choice(stock)
        _yield = 0
        best_solution = None
        best_stock = None
        for stock_size in stock:
            solution_pieces = []
            count = 0
            while stock_size - piece_sum(solution_pieces) >= piece[piece_mapping[position]] and position >= 0:
                item = piece[piece_mapping[position]]
                if stock_size - piece_sum(solution_pieces) >= item:
                    solution_pieces.append(piece_mapping[position])
                    position -= 1
                    count += 1
            print solution_pieces
            if piece_sum(solution_pieces) / stock_size > _yield:
                _yield = piece_sum(solution_pieces) / stock_size
                best_solution = solution_pieces
                best_stock = stock_size
                print "in: %s" % best_solution
            print "best: %s" % best_solution
            position += count
        position = position - len(best_solution)
        item_chromosome.append(best_solution)
        stock_chromosome.append(best_stock)
    return [item_chromosome, stock_chromosome]


def FFD(stock, piece, piece_mapping):
    def piece_sum(piece_map):
        total = 0
        for p in piece_map:
            total += piece[p]
        return total

    item_chromosome = []
    stock_chromosome = []
    copy_piece_map = []
    copy_piece_map[:] = piece_mapping[:]
    # position = len(copy_piece_map) - 1

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

            print "ll : %s | yield: %s"%(float(piece_sum(solution_pieces)) / stock_size,_yield)
            if float(piece_sum(solution_pieces)) / stock_size > _yield:
                _yield = piece_sum(solution_pieces) / stock_size
                # print _yield
                best_solution = solution_pieces
                # print best_solution
                best_stock = stock_size
                print "solution piece: %s" % solution_pieces
        print copy_piece_map
        print "best: %s"%best_solution
        item_chromosome.append(best_solution)
        stock_chromosome.append(best_stock)
        for sol in best_solution:
            copy_piece_map.remove(sol)
            # del copy_piece_map[sol]
        print copy_piece_map
        print "----"


    # while position >= 0:
    #     # for position in piece_mapping:
    #     # random_stock = random.choice(stock)
    #     _yield = 0
    #     best_solution = None
    #     best_stock = None
    #     for stock in stock:
    #         solution_pieces = []
    #         count = 0
    #         while stock - piece_sum(solution_pieces) >= piece[copy_piece_map[position]] and position >= 0:
    #             item = piece[copy_piece_map[position]]
    #             if stock - piece_sum(solution_pieces) >= item:
    #                 solution_pieces.append(copy_piece_map[position])
    #                 position -= 1
    #                 count += 1
    #         print solution_pieces
    #         if piece_sum(solution_pieces) / stock > _yield:
    #             _yield = piece_sum(solution_pieces) / stock
    #             best_solution = solution_pieces
    #             best_stock = stock
    #             print "in: %s" % best_solution
    #         print "best: %s" % best_solution
    #         position += count
    #     position = position - len(best_solution)
    #     item_chromosome.append(best_solution)
    #     stock_chromosome.append(best_stock)
    return [item_chromosome, stock_chromosome]


def FFD1(stock, piece, piece_mapping):
    def piece_sum(piece_map):
        total = 0
        for p in piece_map:
            total += piece[p]
        return total

    item_chromosome = []
    stock_chromosome = []
    copy_piece_map = []
    copy_piece_map[:] = piece_mapping[:]
    copy_piece_map.sort()
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

        item_chromosome.append(best_solution)
        stock_chromosome.append(best_stock)
        for sol in best_solution:
            copy_piece_map.remove(sol)

    return [item_chromosome, stock_chromosome]

# print FFD(STOCK, PIECE, PIECE_map)[1]
# l = [2350, 2350, 2250, 2250, 2250, 2250, 2200, 2200, 2200, 2200, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2100, 2050, 2050, 2050, 2050, 2050, 2050, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 1950, 1950, 1950, 1950, 1950, 1950, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1850, 1700, 1700, 1700, 1700, 1700, 1650, 1650, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1300, 1300, 1300, 1250, 1250, 1250, 1250, 1250, 1250, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1150, 1150, 1150, 1150, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1050, 1050, 1050]

# l1 = [[1100, 1100, 1100], [1900, 1650], [1200, 1200, 1150], [2000, 1700], [1200, 1200, 1150], [2000, 1700], [1200, 1150, 1100], [1250, 1250, 1200], [2000, 1350], [1850, 1850], [2000, 1700], [1100, 1100, 1100], [1850, 1850], [1200, 1200, 1150], [1250, 1200, 1100], [2000, 1350], [2000, 1700], [2000, 1700], [1050, 1050, 1050]]

l1 = [[2000, 1700], [2000, 1700], [2000, 1700], [2000, 1700], [2000, 1700], [2000, 1350], [2000, 1350], [1900, 1650], [1850, 1850], [1850, 1850], [1250, 1250, 1200], [1250, 1200, 1100], [1200, 1200, 1150], [1200, 1200, 1150], [1200, 1200, 1150], [1200, 1150, 1100], [1100, 1100, 1100], [1100, 1100, 1100], [1050, 1050, 1050]]
l2 = [[2350, 1950], [2350, 1950], [2250, 2050], [2250, 2050], [2250, 2050], [2250, 2050], [2200, 2100], [2200, 2100], [2200, 2100], [2200, 2100], [2100, 2050], [2100, 2050], [2100, 1850], [2100, 1850], [2100, 1850], [2100, 1850], [2100, 1850], [2100, 1850], [2100, 1850], [2100, 1850], [2100, 1850], [2000, 1950], [2000, 1950], [2000, 1950], [2000, 1950], [1900, 1900], [1900, 1900], [1900, 1900], [1900, 1900], [1900, 1900], [1900, 1900], [1900, 1900], [1650, 1350, 1300], [1350, 1350, 1250], [1350, 1350, 1250], [1350, 1350, 1250], [1300, 1300, 1200]]
# l2 = [[1900, 1900], [2000, 1950], [1900, 1900], [2200, 2100], [2100, 1850], [2100, 1850], [2200, 2100], [1350, 1350, 1250], [1900, 1900], [2250, 2050], [2100, 1850], [1900, 1900], [1650, 1350, 1300], [1300, 1300, 1200], [1900, 1900], [1900, 1900], [2250, 2050], [2250, 2050], [1350, 1350, 1250], [2000, 1950], [2000, 1950], [2000, 1950], [2100, 1850], [2350, 1950], [2100, 2050], [2200, 2100], [2200, 2100], [2100, 1850], [2100, 1850], [2100, 1850], [1350, 1350, 1250], [2100, 2050], [2100, 1850], [1900, 1900], [2350, 1950], [2250, 2050], [2100, 1850]]
l = sorted(chain(*(l1+l2)), reverse=True)

for i in l1:
    if sum(i) > 4300:
        print "wrong"
for i in l2:
    if sum(i) > 3500:
        print "wrong"
quantities = []
for p in sorted(set(l),reverse=True):
    quantities.append(l.count(p))
print("Quantities:    %s" % quantities)
print quantities == [2, 4, 4, 15, 6, 11, 6, 15, 13, 5, 2, 9, 3, 6, 10, 4, 8, 3]
print len(l) == sum([2, 4, 4, 15, 6, 11, 6, 15, 13, 5, 2, 9, 3, 6, 10, 4, 8, 3])
print len(l1)*86+len(l2)*63 == 3965

# STOCK3 = (120, 115, 110, 105, 100)
# PRICE3 = {120: 12, 115: 11.5, 110: 11, 105: 10.5, 100: 10}
# PIECE3 = [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
#               22, 22, 24, 24, 24, 24, 24, 24, 24, 25, 25, 25, 25, 25, 27, 27, 27, 27, 27, 27, 27, 27, 27, 29, 29, 29,
#               29, 29, 29, 29, 29, 29, 30, 30, 30, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 32, 32,
#               32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33,
#               33, 33, 33, 33, 33, 33, 33, 34, 34, 34, 34, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35,
#               35, 35, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 39, 39, 39, 39,
#               39, 39, 39, 39, 39, 42, 42, 42, 42, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44,
#               44, 44, 45, 45, 45, 45, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 47, 47, 47, 47, 47, 47, 47, 47,
#               47, 47, 47, 47, 47, 47, 47, 48, 48, 48, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49,
#               49, 49, 49, 49, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 51, 51, 51, 51, 51, 51, 51, 51,
#               51, 51, 51, 51, 51, 51, 51, 52, 52, 52, 52, 52, 52, 53, 53, 53, 53, 54, 54, 54, 54, 54, 54, 54, 55, 55,
#               55, 55, 55, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 57, 57, 57, 57,
#               57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 59, 59, 59, 59, 59, 59, 60, 60, 60, 61, 61,
#               61, 61, 61, 61, 61, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 65,
#               65, 65, 65, 65, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67,
#               67, 67, 67, 67, 67]
# PIECE_map3 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394]
#
# item, stock = FFD1(STOCK3,PIECE3,PIECE_map3)
# print item
# print stock
# cost = 0
# for i in stock:
#     cost += PRICE3[i]
# print cost
#testing code
# replace()
# for i1,i2 in range(0,5):
#     print i1,i2

# l1 = [1,2]
# l2 = [3,4]
#
# l1[0], l2[0] = l2[0], l1[0]
#
# print l1, l2
