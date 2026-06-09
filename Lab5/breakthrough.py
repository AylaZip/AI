import sys
from typing import Self

EMPTY = 0
WHITE = 1
BLACK = -1

SIZE = 8

PIECE_SYMBOLS = {EMPTY: '.', WHITE: 'W', BLACK: 'B'}
PLAYER_NAMES = {WHITE: 'White', BLACK: 'Black'}

type Board = tuple[tuple[int, ...], ...]
type State = tuple[Board, int]

initial_board: Board = (
    (WHITE,) * SIZE,
    (WHITE,) * SIZE,
    (EMPTY,) * SIZE,
    (EMPTY,) * SIZE,
    (EMPTY,) * SIZE,
    (EMPTY,) * SIZE,
    (BLACK,) * SIZE,
    (BLACK,) * SIZE,
)


def is_terminal(state: State) -> bool:
    board, _ = state
    if any(cell == WHITE for cell in board[7]):
        return True
    if any(cell == BLACK for cell in board[0]):
        return True
    white_count = sum(row.count(WHITE) for row in board)
    black_count = sum(row.count(BLACK) for row in board)
    return white_count == 0 or black_count == 0


def utility_of(state: State) -> int:
    board, _ = state
    if any(cell == WHITE for cell in board[7]):
        return 1
    if any(cell == BLACK for cell in board[0]):
        return -1
    white_count = sum(row.count(WHITE) for row in board)
    black_count = sum(row.count(BLACK) for row in board)
    if white_count == 0:
        return -1
    if black_count == 0:
        return 1
    return 0


def evaluate(board: Board) -> float:
    white_score = 0.0
    black_score = 0.0
    for r in range(SIZE):
        for c in range(SIZE):
            piece = board[r][c]
            if piece == WHITE:
                white_score += 1.0 + r * 0.1
            elif piece == BLACK:
                black_score += 1.0 + (SIZE - 1 - r) * 0.1
    return white_score - black_score


def _moves_for_piece(board: Board, r: int, c: int, player: int) -> list[tuple[Board, int, int]]:
    out = []
    direction = 1 if player == WHITE else -1
    nr = r + direction
    if not (0 <= nr < SIZE):
        return out
    for nc in (c - 1, c, c + 1):
        if not (0 <= nc < SIZE):
            continue
        target = board[nr][nc]
        if nc == c:
            if target != EMPTY:
                continue
        else:
            if target == player:
                continue
        new_row = list(board[nr])
        new_row[nc] = player
        old_row = list(board[r])
        old_row[c] = EMPTY
        new_board = list(board)
        new_board[r] = tuple(old_row)
        new_board[nr] = tuple(new_row)
        out.append((tuple(new_board), r, c))
    return out


def successors_of(state: State) -> list[State]:
    board, turn = state
    out = []
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == turn:
                for new_board, _, _ in _moves_for_piece(board, r, c, turn):
                    out.append((new_board, -turn))
    return out


def display(board: Board):
    print('  ' + ' '.join(str(c) for c in range(SIZE)))
    for r in range(SIZE):
        row_str = ' '.join(PIECE_SYMBOLS[cell] for cell in board[r])
        print(f'{r} {row_str}')


def alpha_beta_decision(state: State, max_depth: int = 6) -> State | None:
    infinity = float('inf')

    def max_value(s: State, alpha: float, beta: float, depth: int) -> float:
        if is_terminal(s):
            return utility_of(s)
        if depth == 0:
            return evaluate(s[0])
        v = -infinity
        for succ in successors_of(s):
            v = max(v, min_value(succ, alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(s: State, alpha: float, beta: float, depth: int) -> float:
        if is_terminal(s):
            return utility_of(s)
        if depth == 0:
            return evaluate(s[0])
        v = infinity
        for succ in successors_of(s):
            v = min(v, max_value(succ, alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best = None
    best_val = -infinity
    for succ in successors_of(state):
        val = min_value(succ, -infinity, infinity, max_depth - 1)
        if val > best_val:
            best_val = val
            best = succ
    return best


def user_move(state: State) -> State:
    board, turn = state
    print(f'\n{PLAYER_NAMES[turn]}\'s turn')
    display(board)

    moves = successors_of(state)
    for i, (b, _) in enumerate(moves):
        for r in range(SIZE):
            for c in range(SIZE):
                if b[r][c] != board[r][c]:
                    old = board[r][c]
                    if b[r][c] == turn:
                        print(f'{i}: Move to ({r},{c})')
                    elif old == turn:
                        print(f'{i}: Move from ({r},{c})')

    choice = int(input('Select move: '))
    return moves[choice]


def main():
    state = (initial_board, WHITE)

    while not is_terminal(state):
        board, turn = state
        if turn == WHITE:
            state = alpha_beta_decision(state)
            if state is None:
                break
            print(f'\nComputer ({PLAYER_NAMES[turn]}) moved:')
        else:
            state = user_move(state)

    board, _ = state
    display(board)
    winner = PLAYER_NAMES[WHITE] if utility_of(state) == 1 else PLAYER_NAMES[BLACK]
    print(f'\nWinner: {winner}')


if __name__ == '__main__':
    main()
