import random
import time
import sys, os
from typing import Self

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from framework.ga import Individual, genetic_algorithm
from homework.queens_fitness import fitness_fn_negative

p_mutation = 0.5
p_value_mutation = 0.5
num_of_generations = 100

type BoardView = tuple[int, int, int, int, int, int, int, int]

class Board(Individual):
    def __init__(self, gene: BoardView):
        self.gene = gene

    def get_fitness(self) -> float:
        return float(fitness_fn_negative(self.gene) + 28)

    def mutate(self) -> Self:
        gene_list = list(self.gene)
        idx = random.randint(0, len(gene_list) - 1)
        gene_list[idx] = random.randint(1, len(gene_list))
        return Board(tuple(gene_list))

    def reproduce(self, other: Self) -> Self:
        crossover = random.randint(1, len(self.gene) - 1)
        child_gene = self.gene[:crossover] + other.gene[crossover:]
        return Board(child_gene)

    def __hash__(self):
        return hash(self.gene)

    @classmethod
    def create_random(cls) -> Self:
        gene = (1, 2, 3, 4, 5, 6, 7, 8)
        for i in range(8):
            gene = gene[:i] + tuple([random.randint(1, 8)]) + gene[i + 1:]
        return cls(gene)

    def __repr__(self) -> str:
        return f"Gene: {self.gene} - Fitness: {self.get_fitness()}"


def get_initial_population(count: int) -> set[Board]:
    """
    Randomly generate count individuals of 8 queens on a board.
    Note since it uses a set it disregards duplicate elements.
    """
    out: set[Board] = set()
    while len(out) < count:
        out.add(Board.create_random())
    return out


def test():
    print(Board((1, 2, 3, 4, 5, 6, 7, 8)).get_fitness())


def main():
    minimal_fitness = 28

    initial_population = get_initial_population(8)

    start_time = time.perf_counter_ns()
    fittest = genetic_algorithm(initial_population, minimal_fitness,
                                num_of_generations, should_trim_population=True)
    end_time = time.perf_counter_ns()

    if fittest:
        print(f"Fittest Individual: {fittest} - fitness: {fittest.get_fitness()}")
    else:
        print("No solution found")

    elapsed_time = (end_time - start_time) / 10 ** 6
    print(f"total elapsed time: {elapsed_time} ms")


if __name__ == '__main__':
    main()
    # test()
