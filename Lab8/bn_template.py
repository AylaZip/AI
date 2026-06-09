import functools

from Variable import Variable


def multiply_vector_elements(vector):
    def mult(x, y):
        return x * y

    return functools.reduce(mult, vector, 1)


class BayesianNetwork(object):
    def __init__(self):
        self.variables: list[Variable] = []
        self.variable_dictionary: dict[str, Variable] = {}
        self.ready: bool = False

    def calculate_marginal_probabilities(self) -> None:
        for variable in self.variables:
            variable.calculate_marginal_probability()
        self.ready = True

    def get_variables(self) -> list[Variable]:
        return self.variables

    def get_variable(self, variable_name: str) -> Variable:
        return self.variable_dictionary[variable_name]

    def add_variable(self, var: Variable, index: int = -1) -> None:
        if index < 0:
            self.variables.append(var)
        else:
            self.variables.insert(index, var)
        self.variable_dictionary[var.name] = var
        self.ready = False

    def set_variables(self, new_variables: list[Variable]) -> None:
        self.variables = new_variables
        for variable in self.variables:
            self.variable_dictionary[variable.name] = variable
        self.ready = False
        self.calculate_marginal_probabilities()

    def get_marginal_probability(self, var: Variable, val: str) -> float:
        return var.get_marginal_probability(val)

    def get_joint_probability(self, values: dict[str, str]) -> float:
        prob = 1.0
        for var in self.variables:
            var_value = values[var.name]
            parent_values = tuple(values[p.name] for p in var.parents)
            prob *= var.get_probability(var_value, parent_values)
        return prob

    def get_conditional_probability(self, values: dict[str, str], evidents: dict[str, str]) -> float:
        res: float = 1
        first_val = list(values.keys())[0]
        first_variable = self.variable_dictionary[first_val]
        if all(first_variable.is_child_of(self.variable_dictionary[evident]) for evident in evidents.keys()):
            for child, c_val in values.items():
                res *= self.variable_dictionary[child].get_conditional_probability(c_val, evidents)
        else:
            print('probability of parents given their children')

            joint_marginal_parents = 1
            joint_marginal_children = 1
            joint_conditional_children = 1
            marginal_of_evidents = 1

            for parent, p_val in values.items():
                joint_marginal_parents *= self.variable_dictionary[parent].get_marginal_probability(p_val)
            for child, c_val in evidents.items():
                joint_marginal_children *= self.variable_dictionary[child].get_marginal_probability(c_val)
                joint_conditional_children *= self.variable_dictionary[child].get_conditional_probability(c_val, values)

                k = list(values.keys())[0]
                complementary_conditional_values = values.copy()
                complementary_conditional_values[k] = 'false' if values[k] == 'true' else 'true'
                marginal_of_evidents = marginal_of_evidents * self.variable_dictionary[
                    child].get_conditional_probability(c_val, complementary_conditional_values)

            res = (joint_conditional_children * joint_marginal_parents) / (
                    (joint_conditional_children * joint_marginal_parents) + marginal_of_evidents *
                    (1 - joint_marginal_parents))

        return res

    def sub_vals(self, var: Variable, values: dict[str, str]) -> tuple[str, ...]:
        sub = []
        for p in var.parents:
            sub.append(values[p.name])
        return tuple(sub)
