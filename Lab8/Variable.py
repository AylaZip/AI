from typing import Self


class Variable(object):
    def __init__(self, name: str, assignments: tuple[str, ...],
                 probability_table: dict[tuple[str, ...], tuple[float, ...]], parents: list[Self] = None,
                 children: list[Self] = None):
        if parents is None:
            parents = []

        self.name = name
        self.assignments: dict[str, int] = {}
        for i in range(len(assignments)):
            self.assignments[assignments[i]] = i

        for key, val in probability_table.items():
            if len(val) != len(assignments):
                raise ValueError('data in probability table is inconsistent with possible assignments')

        self.probability_table: dict[tuple[str, ...], tuple[float, ...]] = probability_table
        self.children: list[Variable] = children if children is not None else []
        self.parents: list[Variable] = parents
        self.marginal_probabilities: list[float] = len(assignments) * [0]
        self.ready: bool = False

        self.calculate_marginal_probability()

    def get_name(self) -> str:
        return self.name

    def get_assignments(self) -> dict[str, int]:
        return self.assignments

    def get_assignment_index(self, assignment: str) -> int:
        return self.assignments[assignment]

    def get_probability(self, value: str, parents_values: tuple[str, ...]) -> float:
        return self.probability_table[parents_values][self.assignments[value]]

    def get_conditional_probability(self, value: str, parents_values: dict[str, str]) -> float:
        res: float = 0
        given_parents_index = []
        marginal_parents_index = []
        for i, v in enumerate(self.parents):
            if v.name in parents_values:
                given_parents_index.append((i, parents_values[v.name]))
            else:
                marginal_parents_index.append(i)

        for row_key, row_val in self.probability_table.items():
            valid_row = 1
            for gpi in given_parents_index:
                if row_key[gpi[0]] != gpi[1]:
                    valid_row = 0
                    break
            if valid_row:
                parents_probability = 1
                for mpi in marginal_parents_index:
                    parents_probability *= self.parents[mpi].get_marginal_probability(row_key[mpi])
                res += row_val[self.assignments[value]] * parents_probability
        return res

    def calculate_marginal_probability(self):
        if self.ready:
            return

        import itertools

        for i in range(len(self.marginal_probabilities)):
            total = 0.0
            if not self.parents:
                total = self.probability_table[()][i]
            else:
                parent_assign_lists = [list(p.assignments.keys()) for p in self.parents]
                for parent_vals in itertools.product(*parent_assign_lists):
                    parent_prob = 1.0
                    for j, p in enumerate(self.parents):
                        parent_prob *= p.get_marginal_probability(parent_vals[j])
                    total += self.probability_table[parent_vals][i] * parent_prob
            self.marginal_probabilities[i] = total

        self.ready = True

    def get_marginal_probability(self, val: str) -> float:
        return self.marginal_probabilities[self.assignments[val]]

    def add_child(self, node):
        self.children.append(node)

    def add_parent(self, node):
        self.parents.append(node)

    def get_parents(self):
        return self.parents

    def get_children(self):
        return self.children

    def is_child_of(self, node):
        for var in self.parents:
            if var.name == node.name:
                return 1
        return 0
