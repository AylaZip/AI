import numpy as np
from numpy import ndarray

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a description of the number
of ice cream eaten by a boy in the summer.
"""


def main():
    np.set_printoptions(suppress=True)

    states = np.array(["initial", "hot", "cold", "final"])

    # To simulate starting from index 1, we add a dummy value at index 0
    # observation_sets = [
    #     [None, 3, 1, 3],
    #     [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
    #     [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    # ]
    observation_sets = [
        [None, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    ]

    # Markov transition matrix
    #
    # prob_of_next = transitions[current][next]
    # index 0 = start
    # index 1 = hot
    # index 2 = cold
    # index 3 = end      to:  S   h   c   e     from:
    transitions = np.array([[.0, .8, .2, .0],  # Initial state
                            [.0, .2, .6, .2],  # Hot state
                            [.0, .3, .5, .2],  # Cold state
                            [.0, .0, .0, .0],  # Final state
                            ])

    # P(v|q)
    # emission[state][observation]
    # probality_of_this_amount_of_icecreams_given_weather = emission[state (weather)][observation (number of icecreams)]
    #                      0    1   2   3
    emissions = np.array([[.0, .0, .0, .0],  # Initial state
                          [.0, .1, .15, .75],  # Hot state
                          [.0, .8, .1, .1],  # Cold state
                          [.0, .0, .0, .0],  # Final state
                          ])

    for observations in observation_sets:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))

        probability = compute_forward(states, observations, transitions, emissions)
        print("Probability: {}".format(probability))

        path = compute_viterbi(states, observations, transitions, emissions)
        print(f"Path: {convert_path_states_to_observations(path, states)}")

        print('')


def convert_path_states_to_observations(path: list[int], states: ndarray[str]) -> list[str]:
    return [states[p] for p in path]


def inclusive_range(a: int, b: int) -> range:
    return range(a, b + 1)


def compute_forward(states: ndarray, observations: list[int | None], a_transitions: ndarray,
                    b_emissions: ndarray[float]) -> float:
    big_n = len(states) - 2
    big_t = len(observations) - 1
    qf = big_n + 1

    forward = np.ones((big_n + 2, big_t + 1)) * 5

    for j in inclusive_range(1, big_n):
        forward[j][1] = a_transitions[0][j] * b_emissions[j][observations[1]]

    for t in inclusive_range(2, big_t):
        for j in inclusive_range(1, big_n):
            s = 0.0
            for i in inclusive_range(1, big_n):
                s += forward[i][t - 1] * a_transitions[i][j]
            forward[j][t] = s * b_emissions[j][observations[t]]

    prob = 0.0
    for i in inclusive_range(1, big_n):
        prob += forward[i][big_t] * a_transitions[i][qf]

    return prob


def compute_viterbi(states: ndarray, observations: list[int | None], a_transitions: ndarray, b_emissions: ndarray):
    big_n = len(states) - 2
    big_t = len(observations) - 1
    qf = big_n + 1

    viterbi = np.ones((big_n + 2, big_t + 1)) * 5
    backpointers = np.ones((big_n + 2, big_t + 1), dtype=int) * 5

    for j in inclusive_range(1, big_n):
        viterbi[j][1] = a_transitions[0][j] * b_emissions[j][observations[1]]
        backpointers[j][1] = 0

    for t in inclusive_range(2, big_t):
        for j in inclusive_range(1, big_n):
            best_i = argmax([(i, viterbi[i][t - 1] * a_transitions[i][j]) for i in inclusive_range(1, big_n)])
            viterbi[j][t] = viterbi[best_i][t - 1] * a_transitions[best_i][j] * b_emissions[j][observations[t]]
            backpointers[j][t] = best_i

    best_last = argmax([(i, viterbi[i][big_t] * a_transitions[i][qf]) for i in inclusive_range(1, big_n)])
    path = [best_last]
    for t in range(big_t, 1, -1):
        path.insert(0, backpointers[path[0]][t])

    return path


def argmax(sequence: list[tuple[float, float]]):
    '''
    This takes in a list, that provides its own keys as tuples.
    As such the following must hold true:
    sequence[i] = tuple(key, value)
    '''
    # I have rewritten this function slightly, to make it make better sense in my head
    return max(sequence, key=lambda x: x[1])[0]


if __name__ == '__main__':
    main()
