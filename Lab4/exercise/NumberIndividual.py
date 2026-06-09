import random
import sys, os
from typing import Self, override

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from framework.ga import Individual, genetic_algorithm


class NumberIndividual(Individual):
    def __init__(self, gene: tuple):
        self.gene = gene

    @override
    def get_fitness(self) -> float:
        value = 0
        for i, bit in enumerate(reversed(self.gene)):
            value += bit * (2 ** i)
        return float(value)

    @override
    def mutate(self) -> Self:
        gene_list = list(self.gene)
        idx = random.randint(0, len(gene_list) - 1)
        gene_list[idx] = 1 - gene_list[idx]
        return NumberIndividual(tuple(gene_list))

    @override
    def reproduce(self, other: Self) -> Self:
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
    if count > 2 ** n:
        raise ValueError("Count must be less than 2^n, otherwise not enough unique individuals can be generated.")
    out: set[NumberIndividual] = set()
    while len(out) < count:
        out.add(NumberIndividual.create_random(n))
    return out


def main():
    minimal_fitness = 7
    initial_population = {
        NumberIndividual((1, 1, 0)),
        NumberIndividual((0, 0, 0)),
        NumberIndividual((0, 1, 0)),
        NumberIndividual((1, 0, 0))
    }
    fittest = genetic_algorithm(initial_population, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    main()
