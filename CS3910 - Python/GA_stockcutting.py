import bisect


class SolutionChromosome:
    def __init__(self):
        chromosome = []
        age = 0
        fitness = self.__evaluate()

    def age(self):
        self.age += 1

    def __evaluate(self):
        return 0


class PatternChromosome:
    PRICE = None

    def __init__(self):
        pattern = []
        fitness = self.__evaluate()

    def __evaluate(self, penalty):
        waste = self.waste
        return PatternChromosome.PRICE[self.stock_size] + waste * penalty if waste >= 0 else 99999

    def __update_waste(self):
        self.pattern[-1] = self.pattern[0] - sum(self.pattern[1:-1])

    @property
    def stock_size(self):
        return self.pattern[0]

    @property
    def waste(self):
        return self.pattern[-1]
