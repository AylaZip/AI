from collections.abc import Iterable
from typing import Callable

# This is based on the game Nim, where each player must in turn select a pile to split.
# The result of the split must be 2 piles of different sizes

type Piles = list[int]


def alpha_beta_decision(state: Piles) -> list[int]:
    infinity = float('inf')

    def max_value(state_option: Piles, alpha: float, beta: float) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        expected_value = -infinity
        for successor in successors_of(state_option):
            expected_value = max(expected_value, min_value(successor, alpha, beta))
            if expected_value >= beta:
                return expected_value
            alpha = max(alpha, expected_value)
        return expected_value

    def min_value(state_option: Piles, alpha: float, beta: float) -> int:
        if is_terminal(state_option):
            return utility_of(state_option)
        v = infinity

        for successor in successors_of(state_option):
            v = min(v, max_value(successor, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    state = argmax(
        successors_of(state),
        lambda a: min_value(a, -infinity, infinity)
    )
    return state


PLAY_FOR_MIN = False


def is_terminal(state: Piles) -> bool:
    return all(pile <= 2 for pile in state)


def utility_of(state: Piles) -> int:
    if len(state) % 2 == 0:
        return 1 if PLAY_FOR_MIN else -1
    else:
        return -1 if PLAY_FOR_MIN else 1


def successors_of(state: Piles) -> list[Piles]:
    out = []
    for i, pile in enumerate(state):
        if pile >= 3:
            for split in split_pile_options(pile):
                new_state = state[:i] + split + state[i + 1:]
                out.append(new_state)
    return out


def split_pile_options(pile: int) -> list[Piles]:
    out = []
    for i in range(1, (pile + 1) // 2):
        out.append([i, pile - i])
    return out


def argmax(iterable: Iterable, func: Callable[[Piles], int]):
    return max(iterable, key=func)


def computer_select_pile(state: Piles) -> Piles:
    return alpha_beta_decision(state)


def user_select_pile(list_of_piles: Piles) -> Piles:
    """
    Given a list of piles, asks the user to select a pile and then a split.
    Then returns the new list of piles.
    """
    print("\n    Current piles: {}".format(list_of_piles))

    i = -1
    while i < 0 or i >= len(list_of_piles) or list_of_piles[i] < 3:
        print("What is the number of the pile you want to split?")
        print("The pile must have more than 2 stones")
        print(f"Choose a number between 1 and {len(list_of_piles)}")
        i = -1 + int(input())

    print("Selected pile {}".format(list_of_piles[i]))

    max_split = list_of_piles[i] - 1

    j = 0
    while j < 1 or j > max_split or j == list_of_piles[i] - j:
        print_str = f"Where should the first split be (from 1 to {max_split}"
        if list_of_piles[i] % 2 == 0:
            print_str += f", but not {list_of_piles[i] // 2}"

        print_str += ")?"
        print(print_str)

        j = int(input())

    k = list_of_piles[i] - j

    new_list_of_piles = list_of_piles[:i] + [j, k] + list_of_piles[i + 1:]

    print("    New piles: {}".format(new_list_of_piles))

    return new_list_of_piles


def main():
    state = [7]

    while not is_terminal(state):
        state = user_select_pile(state)
        if not is_terminal(state):
            state = computer_select_pile(state)
            print("The computer has split a pile")

    print("    Final state is {}".format(state))


def main_min():
    global PLAY_FOR_MIN
    PLAY_FOR_MIN = True
    state = [7]

    while not is_terminal(state):
        state = computer_select_pile(state)
        print("The computer (MIN) has split a pile")
        if not is_terminal(state):
            state = user_select_pile(state)

    print("    Final state is {}".format(state))


if __name__ == '__main__':
    main()
    # main_min()  # uncomment for homework task 3 (play as MIN)
