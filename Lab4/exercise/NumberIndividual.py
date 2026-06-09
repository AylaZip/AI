import random
import sys, os
from typing import Self, override

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from framework.ga import Individual, genetic_algorithm


##########################
# Instruction:
# Run this file directly for the exercise.
#
##########################

class NumberIndividual(Individual):
    def __init__(self, gene: tuple):
        self.gene = gene

    @override
    def get_fitness(self) -> float:
        """
        Computes the decimal value of the individual
        Return the fitness level of the individual

        Explanation:
        enumerate(list) returns a list of pairs (position, element):

        enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]

        enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
        """

        #raise NotImplementedError("Your task is to fix this: Fitness function should be implemented in NumberIndividual class.")
        value = 0
        for i, bit in enumerate(reversed(self.gene)):
            value += bit * (2 ** i)
        return float(value)

    @override
    def mutate(self) -> Self:
        #raise NotImplementedError("Your task is to fix this: Mutation should be implemented in NumberIndividual class.")
        gene_list = list(self.gene)
        idx = random.randint(0, len(gene_list) - 1)
        gene_list[idx] = 1 - gene_list[idx]
        return NumberIndividual(tuple(gene_list))


    @override
    def reproduce(self, other: Self) -> Self:
        """
       Reproduce this individual with another with single-point crossover
       Return the child individual
       """
        #raise NotImplementedError("Your task is to fix this: Reproduction should be implemented in NumberIndividual class.")
        crossover = random.randint(1, len(self.gene) - 1)
        child_gene = self.gene[:crossover] + other.gene[crossover:]
        return NumberIndividual(child_gene)

    def __hash__(self):
        return hash(self.gene)

    @classmethod
    def create_random(cls, length_of_gene: int) -> Self:
        return cls(tuple(random.randint(0, 1) for _ in range(length_of_gene)))

    def __repr__(self) -> str:
        return f"Gene: {self.gene} - Fitness: {self.get_fitness()}"


def get_initial_population(n: int, count: int) -> set[NumberIndividual]:
    """
    Randomly generate count individuals of length n
    Note since it's a set it disregards duplicate elements.

    Be aware that since the individuals are generated randomly, but duplicates are not allowed.
    It can take a long time if you use large numbers of count and n together.
    """

    if count > 2 ** n:
        raise ValueError("Count must be less than 2^n, otherwise not enough unique individuals can be generated.")

    out: set[NumberIndividual] = set()

    while len(out) < count:
        out.add(NumberIndividual.create_random(n))

    return out


def main():
    minimal_fitness = 7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        NumberIndividual((1, 1, 0)),
        NumberIndividual((0, 0, 0)),
        NumberIndividual((0, 1, 0)),
        NumberIndividual((1, 0, 0))
    }
    # initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    main()
