import sys, os
from typing import Self, override

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from framework.ga import genetic_algorithm
from exercise.NumberIndividual import NumberIndividual


class SpecificNumberIndividual(NumberIndividual):
    @override
    def get_fitness(self) -> float:
        value = 0
        for i, bit in enumerate(reversed(self.gene)):
            value += bit * (2 ** i)
        return float(7 - abs(value - 4))


def main():
    minimal_fitness = 7

    initial_population = {
        SpecificNumberIndividual((0, 0, 0)),
        SpecificNumberIndividual((0, 0, 1)),
        SpecificNumberIndividual((0, 1, 1)),
        SpecificNumberIndividual((1, 0, 0)),
    }

    fittest = genetic_algorithm(initial_population, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    main()
