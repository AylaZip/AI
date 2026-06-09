from typing import Self, Any
import heapq

# For this lab we will not be able to fully type the state
# The reason for this is that we wanted a fairly simple implementation for the searcher.
# But we still wanted this searcher to be able to handle all 3 different scenarios.
# Feel free to take it as a challenge to make a strongly typed implementation, that can handle all 3 scenarios.
# Consider doing something that could let the statespace generate the states, and decide what next possible states are.

class StateSpace:
    def __init__(self, state_space: dict = None):
        self.state_space = state_space

    def successor(self, state: Any):
        if self.state_space is None:
            print("No state space set")

        return self.state_space[state]


class Node:
    def __init__(self, state: Any, parent: Self = None, depth: int = 0, cost=0):
        self.state = state
        self.parent_node = parent
        self.depth = depth
        self.cost = cost

    def path(self) -> list[Self]:
        current_node = self
        path = [self]
        while current_node.parent_node:
            current_node = current_node.parent_node
            path.append(current_node)

        return list(reversed(path))

    def expand(self, state_space: StateSpace):
        successors: list[Node] = []
        children = state_space.successor(self.state)
        for child, edge_cost in children:
            s = Node(child, self, self.depth + 1, self.cost + edge_cost)
            successors = insert(s, successors)

        return successors

    def display(self) -> None:
        print(self)

    def __repr__(self):
        return f"State: {self.state} - Depth: {self.depth}"


def insert(node: Node, queue: list[Node], insert_as_first: bool = True) -> list[Node]:
    new_queue = queue.copy()
    if insert_as_first:
        new_queue.insert(0,node)
    else:
        new_queue.append(node)
    return new_queue


def insert_all(nodes_to_add: list[Node], queue: list[Node], insert_as_first: bool = True) -> list[Node]:
    new_queue = queue.copy()
    for node in nodes_to_add:
        new_queue = insert(node, new_queue, insert_as_first)
    return new_queue


def remove_first(queue: list[Node]) -> Node:
    # Hint this function is really short, and you can probably do it in one line
    return queue.pop(0)


class Searcher:
    def __init__(self, initial_state, goal_state, state_space: StateSpace = None, heuristic=None):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state_space = state_space
        self.heuristic = heuristic or (lambda s: 0)

    def tree_search(self, search_type="astar", weight=1.0):
        fringe = []
        counter = 0
        initial_node = Node(self.initial_state, cost=0)
        h = self.heuristic(self.initial_state)

        if search_type == "gbfs":
            priority = h 
        elif search_type == "weighted_astar":
            priority = initial_node.cost + weight * h
        else:
            priority = initial_node.cost + h

        heapq.heappush(fringe, (priority, counter, initial_node))
        counter += 1
        visited = set()
        nodes_explored = 0

        while fringe:
            _, _, node = heapq.heappop(fringe)

            if node.state in visited:
                continue
            visited.add(node.state)
            nodes_explored += 1

            if node.state == self.goal_state:
                return node.path(), nodes_explored

            for child in node.expand(self.state_space):
                if child.state not in visited:
                    h = self.heuristic(child.state)
                    if search_type == "gbfs":
                        priority = h
                    elif search_type == "weighted_astar":
                        priority = child.cost + weight * h
                    else:
                        priority = child.cost + h
                    heapq.heappush(fringe, (priority, counter, child))
                    counter += 1

        return None, nodes_explored

    def run(self, insert_as_first: bool = True):
        path = self.tree_search(insert_as_first)
        print("Solution path:")
        for node in path:
            node.display()

class FunctionStateSpace(StateSpace):
    def __init__(self, successor_fn):
        self.successor_fn = successor_fn
    def successor(self, state):
        return self.successor_fn(state)

if __name__ == '__main__':
    graph = {
        'A': [('B',1), ('C',2), ('D',4)],
        'B': [('E',4), ('F',5)],
        'C': [('E',1)],
        'D': [('H',1), ('I',4), ('J',2)],
        'E': [('G',2), ('H',3)],
        'F': [('G',1)],
        'G': [('K',6)],
        'H': [('K',6), ('L',5)],
        'I': [('L',3)],
        'J': [], 'K': [], 'L': [],
    }
    heuristic = {
        'A':6, 'B':5, 'C':5, 'D':2, 'E':4, 'F':5,
        'G':4, 'H':1, 'I':2, 'J':1, 'K':0, 'L':0,
    }
    h_fn = lambda s: heuristic[s]

    for name, stype in [("GBFS","gbfs"), ("A*","astar"), ("Weighted A* (w=2)","weighted_astar")]:
        for goal in ['K', 'L']:
            print(f"\n=== {name} A→{goal} ===")
            s = Searcher('A', goal, StateSpace(graph), h_fn)
            path, explored = s.tree_search(stype, weight=2 if stype=="weighted_astar" else 1)
            print(f"Path: {' → '.join(str(n.state) for n in path)}")
            print(f"Cost: {path[-1].cost}, Explored: {explored}")

    vacuum_space_incomplete = {
        ('A', 'Dirty', 'Dirty'): [('A', 'Clean', 'Dirty'), ('A', 'Dirty', 'Dirty'), ('B', 'Dirty', 'Dirty')],
        ('B', 'Dirty', 'Dirty'): [('B', 'Dirty', 'Clean'), ('B', 'Dirty', 'Dirty'), ('A', 'Dirty', 'Dirty')],
        ('A', 'Dirty', 'Clean'): [('A', 'Clean', 'Clean'), ('A', 'Dirty', 'Clean'), ('B', 'Dirty', 'Clean')],
        ('A', 'Clean', 'Dirty'): [('A', 'Clean', 'Dirty'), ('A', 'Clean', 'Dirty'), ('B', 'Clean', 'Dirty')],
        ('A', 'Clean', 'Clean'): [('A', 'Clean', 'Clean'), ('A', 'Clean', 'Clean'), ('B', 'Clean', 'Clean')],
        ('B', 'Dirty', 'Clean'): [('B', 'Dirty', 'Clean'), ('B', 'Dirty', 'Clean'), ('A', 'Dirty', 'Clean')],
        ('B', 'Clean', 'Dirty'): [('B', 'Clean', 'Clean'), ('B', 'Clean', 'Dirty'), ('A', 'Clean', 'Dirty')],
        ('B', 'Clean', 'Clean'): [('B', 'Clean', 'Clean'), ('B', 'Clean', 'Clean'), ('A', 'Clean', 'Clean')],
    }

    vacuum_costs = {}

    for state, successors in vacuum_space_incomplete.items():
        vacuum_costs[state] = [(s, 1) for s in successors]

    def vacuum_h(state):
        _, a, b = state
        return (a == 'Dirty') + (b == 'Dirty')

    for goal in [('A', 'Clean', 'Clean'), ('B', 'Clean', 'Clean')]:
        print(f"\n=== A* Vacuum -> {goal} ===")
        s = Searcher(('A', 'Dirty', 'Dirty'), goal, StateSpace(vacuum_costs), vacuum_h)
        path, explored = s.tree_search("astar")
        if path:
            print(f"Steps: {len(path)-1}, Cost: {path[-1].cost}, Explored: {explored}")
            for n in path:
                print(f"  {n.state}")