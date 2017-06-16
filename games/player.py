from collections import Counter, defaultdict, OrderedDict
import random


class OrderedCounter(Counter, OrderedDict):
    pass


def get_actual_next_guess(choices):
    if len(choices) == 0:
        return None

    most_common_guesses = []
    most_common_count = None
    for guess, count in _most_common(choices):
        if most_common_count is None:
            most_common_count = count
            most_common_guesses.append(guess)
        elif most_common_count == count:
            most_common_guesses.append(guess)
        else:
            break
    return random.choice(sorted(most_common_guesses))


def _most_common(counter):
    counter = OrderedCounter(counter)
    for guess, count in counter.most_common():
        yield guess, count
