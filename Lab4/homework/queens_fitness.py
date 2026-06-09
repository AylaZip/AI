def fitness_fn_negative(board_view: tuple[int, ...]):
    n = len(board_view)
    fitness = 0
    for column, row in enumerate(board_view):
        for other_column in range(column + 1, n):
            dx = abs(column - other_column)
            dy = abs(row - board_view[other_column])
            if dx == dy or dy == 0:
                fitness += 1
    return -fitness
