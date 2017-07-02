from collections import Counter, OrderedDict
from decimal import Decimal
import random

import numpy as np

from games import entropy


class OrderedCounter(Counter, OrderedDict):
    pass


def _get_pmf_for_entropy(possible_responses):
    counter = OrderedCounter()
    seen_words = set()
    for response, code_words in possible_responses.items():
        assert code_words.isdisjoint(seen_words), 'There should not be duplicate code words across responses'
        seen_words |= code_words
        counter[response] = Decimal(len(code_words))
    return entropy.get_pmf(counter)


def _get_pmf_for_speed(potential_outcomes):
    length = len(potential_outcomes)
    distribution = np.random.dirichlet(np.ones(length), size=1)[0]
    pmf = {}
    for index, (guess, _) in enumerate(potential_outcomes.items()):
        pmf[guess] = Decimal(distribution[index])
    return pmf


def _get_counts(potential_outcomes, success_pmf):
    speed = _get_pmf_for_speed(potential_outcomes)
    common = {}
    entropies = {}
    minimax = {}
    for guess, possible_responses in potential_outcomes.items():
        common_pmf = success_pmf(possible_responses)
        common[guess] = common_pmf['*']
        entropy_pmf = _get_pmf_for_entropy(possible_responses)
        minimax[guess] = entropy.get_inverse_minimax(entropy_pmf)
        entropies[guess] = entropy.get_entropy(entropy_pmf)

    results = {}
    results['speed'] = speed
    results['common'] = common
    results['entropies'] = entropies
    results['minimax'] = minimax
    return results


def build_strategy(info_focus, success_focus, speed_focus=0.0, minimax_focus=0.0, success_pmf=None, should_sort=False):

    def strategy(potential_outcomes, game_log):
        data = _get_counts(potential_outcomes, success_pmf)

        if len(potential_outcomes.all_code_words) == 1:
            return list(potential_outcomes.all_code_words)[0]

        speed = data.get('speed')
        common = data.get('common')
        entropies = data.get('entropies')
        minimax = data.get('minimax')

        choices = {}
        for letter, pmf in entropies.items():
            if speed[letter] == 0.0 and speed_focus == 0.0:
                speed_weight = 1
            else:
                speed_weight = speed[letter]**Decimal(speed_focus)
            if common[letter] == 0.0 and success_focus == 0.0:
                common_weight = 1
            else:
                common_weight = common[letter]**Decimal(success_focus)
            if entropies[letter] == Decimal(0) and info_focus == 0.0:
                entropy_weight = 1
            else:
                entropy_weight = entropies[letter]**Decimal(info_focus)
            if minimax[letter] == Decimal(0) and minimax_focus == 0.0:
                minimax_weight = 1
            else:
                minimax_weight = minimax[letter]**Decimal(minimax_focus)
            choices[letter] = speed_weight * entropy_weight * common_weight * minimax_weight

        next_guess = get_actual_next_guess(choices, game_log, should_sort)
        # print(choices)
        # print(next_guess, choices[next_guess], entropies[next_guess], Decimal(info_focus),
        #       entropies[next_guess] ** Decimal(info_focus))
        return next_guess

    return strategy


def get_actual_next_guess(choices, game_log, should_sort=False):
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
    if should_sort:
        return sorted(most_common_guesses)[0]
    else:
        return random.choice(sorted(most_common_guesses))
