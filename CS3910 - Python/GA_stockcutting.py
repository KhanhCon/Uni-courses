
import bisect


class Chromosome:
    def __init__(self):
        age = 0
        fitness = self.__evaluate()

    def age(self):
        self.age += 1

    def __evaluate(self):
        return 0


