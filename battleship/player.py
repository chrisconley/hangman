import itertools
import random


def get_next_random_guess(possible_boards, game_log):
    guesses = {tuple(l['guess']) for l in game_log}

    # This only works for square boards
    board_width = possible_boards[0].width
    spots = set(itertools.product(range(board_width), repeat=2))

    remaining_choices = spots - guesses
    if len(remaining_choices) == 0:
        return None, []
    return list(random.choice(list(remaining_choices))), possible_boards
