import random

# stock = [{"length":10,"cost":100},{"length":13,"cost":100},{"length":15,"cost":150}]
price = {10:100,13:130,15:150}
stock = (10,13,15)
# pieces = [{"length":3,"quantities":5},{"length":4,"quantities":2},{"length":5,"quantities":1},{"length":6,"quantities":2},{"length":7,"quantities":4},{"length":8,"quantities":2},{"length":9,"quantities":1},{"length":10,"quantities":3}]
piece = [3,3,3,3,3,4,4,5,6,6,7,7,7,7,8,8,9,10,10,10]

# print random.sample(piece,1)
# print len(pieces)

def random_solution(stock, piece):
    solution = []
    copy_piece = []
    copy_piece[:] = piece[:]
    while len(copy_piece) > 0:
        random_stock = random.choice(stock)
        solution_pieces = []
        while len(copy_piece)>0 and random_stock - sum(solution_pieces) >= min(copy_piece):
            random_piece = random.choice(copy_piece)
            if random_stock - sum(solution_pieces) >= random_piece:
                solution_pieces.append(random_piece)
                copy_piece.remove(random_piece)
        solution.append({"length":random_stock,"solution_pieces":solution_pieces})
    return solution

def random_population(population_size,stock,piece):
    population = []
    for i in range(0,population_size):
        population.append(random_solution(stock, piece))
    return population

def solution_cost(solution,price):
    cost = 0
    for i in solution:
        cost += price[i["length"]]
    return cost

print(solution_cost(random_solution(stock,piece),price))

print(range(0,10))
print(random_population(10,stock,piece))

