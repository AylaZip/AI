from enum import Enum
from typing import Self


class Symbols(Enum):
    X = "X"
    O = "O"
    UNPLACED = "i"

    def __str__(self):
        return self.value

    @classmethod
    def placed(cls) -> tuple[Self, Self]:
        return cls.X, cls.O


type Board = list[Symbols]


def minmax_decision(state: Board) -> int:
    def max_value(state_option: Board) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        expected_value = -infinity
        for (a, s) in successors_of(state_option):
            expected_value = max(expected_value, min_value(s))
        return expected_value

    def min_value(state_option: Board) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        expected_value = infinity
        for (a, s) in successors_of(state_option):
            expected_value = min(expected_value, max_value(s))
        return expected_value

    infinity = float('inf')
    action, state = max(successors_of(state), key=lambda a: min_value(a[1]))
    return action


WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def _check_win(state: Board, symbol: Symbols) -> bool:
    return any(all(state[i] == symbol for i in line) for line in WINNING_LINES)


def is_terminal(state: Board) -> bool:
    return (
        _check_win(state, Symbols.X) or
        _check_win(state, Symbols.O) or
        all(cell != Symbols.UNPLACED for cell in state)
    )


def utility_of(state: Board) -> int:
    if _check_win(state, Symbols.X):
        return 1
    if _check_win(state, Symbols.O):
        return -1
    return 0


def successors_of(state: Board) -> list[tuple[int, Board]]:
    x_count = state.count(Symbols.X)
    o_count = state.count(Symbols.O)
    player = Symbols.X if x_count == o_count else Symbols.O

    out = []
    for i, cell in enumerate(state):
        if cell == Symbols.UNPLACED:
            new_state = state.copy()
            new_state[i] = player
            out.append((i, new_state))
    return out


def display(state: list[Symbols]) -> None:
    print("-----")
    for i in range(0, 3):
        for c in range(i * 3, i * 3 + 3):
            print("|", end="")
            symbol = c if state[c] == Symbols.UNPLACED else state[c]
            print(symbol, end="")
        print("|")


def main():
    board = [Symbols.UNPLACED] * 9
    while not is_terminal(board):
        board[minmax_decision(board)] = Symbols.X
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = Symbols.O
    display(board)


if __name__ == '__main__':
    main()
