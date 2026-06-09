from collections import deque
from collections.abc import Callable
from typing import Any

from Colors import Color
from SAMapStates import SAMapStates
from constraints_template import CSP

type SAContraintFunction = Callable[[SAMapStates, Color, SAMapStates, Color], bool]
type SAAssignment = dict[SAMapStates, Color]


class AC3CSP(CSP):
    def __init__(self, variables: list[SAMapStates], domains: dict[SAMapStates, list[Color]],
                 neighbours: dict[SAMapStates, list[SAMapStates]], constraints: dict[SAMapStates, SAContraintFunction]):
        super().__init__(variables, domains, neighbours, constraints)
        self.current_domains: dict[SAMapStates, list[Color]] = {v: d[:] for v, d in domains.items()}

    def recursive_backtracking(self, assignment: SAAssignment) -> dict[SAMapStates, Color] | None:
        if self.is_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                saved_domains = self._save_domains()

                assignment[var] = value
                self.current_domains[var] = [value]

                if self._forward_check(var):
                    if self._ac3():
                        result = self.recursive_backtracking(assignment)
                        if result is not None:
                            return result

                self._restore_domains(saved_domains)
                del assignment[var]
        return None

    def _save_domains(self) -> dict[SAMapStates, list[Color]]:
        return {v: d[:] for v, d in self.current_domains.items()}

    def _restore_domains(self, saved: dict[SAMapStates, list[Color]]):
        self.current_domains = saved

    def _forward_check(self, var: SAMapStates) -> bool:
        var_value = self.current_domains[var][0]
        for neighbour in self.neighbours[var]:
            constraint = self.constraints[var]
            new_domain = [
                v for v in self.current_domains[neighbour]
                if constraint(var, var_value, neighbour, v)
            ]
            if not new_domain:
                return False
            self.current_domains[neighbour] = new_domain
        return True

    def _ac3(self) -> bool:
        queue = deque()
        for var in self.variables:
            for neighbour in self.neighbours[var]:
                queue.append((var, neighbour))

        while queue:
            x, y = queue.popleft()
            if self._revise(x, y):
                if not self.current_domains[x]:
                    return False
                for z in self.neighbours[x]:
                    if z != y:
                        queue.append((z, x))
        return True

    def _revise(self, x: SAMapStates, y: SAMapStates) -> bool:
        removed = False
        constraint = self.constraints[x]
        new_domain = [
            x_val for x_val in self.current_domains[x]
            if any(constraint(x, x_val, y, y_val) for y_val in self.current_domains[y])
        ]
        if len(new_domain) < len(self.current_domains[x]):
            removed = True
            self.current_domains[x] = new_domain
        return removed


def create_south_america_ac3_csp() -> AC3CSP:
    variables = list(SAMapStates)

    values = [Color.Red, Color.Green, Color.Blue, Color.Yellow]
    domains = {v: values[:] for v in variables}

    neighbours: dict[SAMapStates, list[SAMapStates]] = {
        SAMapStates.COSTA_RICA: [SAMapStates.PANAMA],
        SAMapStates.PANAMA: [SAMapStates.COSTA_RICA, SAMapStates.COLOMBIA],
        SAMapStates.COLOMBIA: [SAMapStates.PANAMA, SAMapStates.VENEZUELA, SAMapStates.BRASIL, SAMapStates.ECUADOR, SAMapStates.PERU],
        SAMapStates.VENEZUELA: [SAMapStates.COLOMBIA, SAMapStates.GUYANA, SAMapStates.BRASIL],
        SAMapStates.GUYANA: [SAMapStates.VENEZUELA, SAMapStates.SURINAME, SAMapStates.BRASIL],
        SAMapStates.SURINAME: [SAMapStates.GUYANA, SAMapStates.GUYANE, SAMapStates.BRASIL],
        SAMapStates.GUYANE: [SAMapStates.SURINAME, SAMapStates.BRASIL],
        SAMapStates.ECUADOR: [SAMapStates.COLOMBIA, SAMapStates.PERU],
        SAMapStates.PERU: [SAMapStates.ECUADOR, SAMapStates.COLOMBIA, SAMapStates.BRASIL, SAMapStates.BOLIVIA, SAMapStates.CHILE],
        SAMapStates.BRASIL: [SAMapStates.COLOMBIA, SAMapStates.VENEZUELA, SAMapStates.GUYANA, SAMapStates.SURINAME, SAMapStates.GUYANE, SAMapStates.URUGUAY, SAMapStates.ARGENTINA, SAMapStates.PARAGUAY, SAMapStates.BOLIVIA, SAMapStates.PERU],
        SAMapStates.BOLIVIA: [SAMapStates.PERU, SAMapStates.CHILE, SAMapStates.ARGENTINA, SAMapStates.PARAGUAY, SAMapStates.BRASIL],
        SAMapStates.PARAGUAY: [SAMapStates.BOLIVIA, SAMapStates.ARGENTINA, SAMapStates.BRASIL],
        SAMapStates.CHILE: [SAMapStates.PERU, SAMapStates.BOLIVIA, SAMapStates.ARGENTINA],
        SAMapStates.ARGENTINA: [SAMapStates.CHILE, SAMapStates.BOLIVIA, SAMapStates.PARAGUAY, SAMapStates.BRASIL, SAMapStates.URUGUAY],
        SAMapStates.URUGUAY: [SAMapStates.BRASIL, SAMapStates.ARGENTINA],
    }

    def constraint_function(
        first_variable: SAMapStates, first_value: Color,
        second_variable: SAMapStates, second_value: Color,
    ) -> bool:
        return first_value != second_value or first_variable == second_variable

    constraints = {v: constraint_function for v in variables}

    return AC3CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    csp = create_south_america_ac3_csp()
    result = csp.backtracking_search()
    if result:
        for area, color in sorted(result.items(), key=lambda x: x[0].name):
            print(f"{area.name}: {color.value}")
    else:
        print("No solution found")
