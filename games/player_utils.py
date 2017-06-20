from collections import Counter, defaultdict, OrderedDict
from decimal import Decimal
import random


class OrderedCounter(Counter, OrderedDict):
    pass


def get_actual_next_guess(choices, game_log):
    if len(choices) == 0:
        return None

    most_common_guesses = []
    most_common_count = None
    for guess, count in OrderedCounter(choices).most_common():
        count = count.quantize(Decimal('1e-20'))
        if guess in game_log.guesses:
            continue
        if most_common_count is None:
            most_common_count = count
            most_common_guesses.append(guess)
        elif most_common_count == count:
            most_common_guesses.append(guess)
        else:
            break
    if most_common_count is None:
        return None
    return sorted(most_common_guesses)[0]
