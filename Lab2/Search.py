from typing import Self, Any


class StateSpace:
    def __init__(self, state_space: dict = None):
        self.state_space = state_space

    def successor(self, state: Any):
        if self.state_space is None:
            print("No state space set")

        return self.state_space[state]


class Node:
    def __init__(self, state: Any, parent: Self = None, depth: int = 0):
        self.state = state
        self.parent_node = parent
        self.depth = depth

    def path(self) -> list[Self]:
        current_node = self
        path = [self]
        while current_node.parent_node:
            current_node = current_node.parent_node
            path.append(current_node)

        return path

    def expand(self, state_space: StateSpace):
        successors: list[Node] = []
        children = state_space.successor(self.state)
        for child in children:
            s = Node(child, self, self.depth + 1)
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
    return queue.pop(0)


class Searcher:
    def __init__(self, initial_state, goal_state, state_space: StateSpace = None):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state_space = state_space

    def tree_search(self, insert_as_first: bool = True) -> list[Node]:
        fringe: list[Node] = []
        initial_node = Node(self.initial_state)
        fringe = insert(initial_node, fringe)
        visited: set = set()
        while fringe is not None:
            node = remove_first(fringe)
            if node.state in visited:
                continue
            visited.add(node.state)
            if node.state == self.goal_state:
                return node.path()
            children = node.expand(self.state_space)
            fringe = insert_all(children, fringe, insert_as_first)

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
    input_state_space = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': [],
        'E': [],
        'F': [],
        'G': ['H', 'I', 'J'],
        'H': [],
        'I': [],
        'J': [],
    }

    searcher = Searcher('A', 'J', state_space=StateSpace(input_state_space))
    print("??-first")
    searcher.run(insert_as_first=True)
    print("????-first")
    searcher.run(insert_as_first=False)

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

    searcher2 = Searcher(('A', 'Dirty', 'Dirty'), ('A', 'Clean', 'Clean'), state_space=StateSpace(vacuum_space_incomplete))
    print("\nBFS - Vaccum World")
    searcher2.run(insert_as_first=False)
