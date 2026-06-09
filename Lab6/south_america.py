from collections.abc import Callable

from Colors import Color
from SAMapStates import SAMapStates
from constraints_template import CSP

type SAContraintFunction = Callable[[SAMapStates, Color, SAMapStates, Color], bool]
type SAAssignment = dict[SAMapStates, Color]


def create_south_america_csp() -> CSP:
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

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    csp = create_south_america_csp()
    result = csp.backtracking_search()
    if result:
        for area, color in sorted(result.items(), key=lambda x: x[0].name):
            print(f"{area.name}: {color.value}")
    else:
        print("No solution found")
