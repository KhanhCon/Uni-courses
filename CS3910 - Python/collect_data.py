import GA_group_chromosome,AIS_stock_cutting,csv

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
data3 = {"price": PRICE3,"stock": STOCK3,"piece": PIECE3,}


# geno = ais.run(function_evaluation=500)

# geno2, fitness = ga.run(function_evaluation=500, population_size=100, mutation_rate=0.05)

print 5.51E-35 < 0.05

with open('data10000.csv', 'wb') as csvfile:
    fieldnames = ['GA', 'AIS']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow({'GA': 'GA', 'AIS': 'AIS'})
    for _ in xrange(0,30):
        ais = AIS_stock_cutting.AIS(data3, replacement_number=25, population_size=50, clone_size_factor=3, mutate_constant=0.3)
        ga = GA_group_chromosome.GA(data3)
        aisgeno = ais.run(function_evaluation=500)
        geno2, fitness = ga.run(function_evaluation=500, population_size=100, mutation_rate=0.05)
        writer.writerow({'GA': fitness, 'AIS': aisgeno.fitness})
