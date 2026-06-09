from Search import Searcher, FunctionStateSpace

def flip(side):
    if side == 'W':
        return 'E'
    else:
        return 'W'

def is_valid(state):
    F, W, G, C = state
    if W == G != F:
        return False
    if G == C != F:
        return False
    return True

def fwgc_successor(state):
    F, W, G, C = state
    candidates = [(flip(F), W, G, C)]

    if F == W:
        candidates.append((flip(F), flip(W), G, C))

    if F == G:
        candidates.append((flip(F), W, flip(G), C))

    if F == C:
        candidates.append((flip(F), W, G, flip(C)))

    return [s for s in candidates if is_valid(s)]

initial = ('W', 'W', 'W', 'W')
goal = ('E', 'E', 'E', 'E')

for name, dfs in [("DFS", True), ("BFS", False)]:
    print(f"\n{name} - FWGC")
    s = Searcher(initial, goal, FunctionStateSpace(fwgc_successor))
    s.run(insert_as_first = dfs)