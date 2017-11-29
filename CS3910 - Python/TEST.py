import random, bisect
from itertools import chain

ebins = [[3, 3, 3], [6, 2, 1], [5, 2], [4, 3], [7, 2], [5, 4]]


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


def lsearch(bins, num_of_free_bin, bin_capacity=10):
    bins.sort(key=lambda x: (sum(x), x[0], x[1] if len(x) > 1 else 0, x[2] if len(x) > 2 else 0,x[3] if len(x) > 3 else 0))
    # free_items = bins[0:num_of_free_bin]
    # free_items = [bin[0] for bin in bins[0:num_of_free_bin]]
    free_items = sorted(chain(*bins[0:num_of_free_bin]), reverse=True)
    print bins
    return free_items


print lsearch(ebins, 2)
