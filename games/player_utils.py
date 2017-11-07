from collections import Counter, OrderedDict, defaultdict
import copy
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
    distribution = np.random.uniform(0.0, 1.0, length)
    pmf = {}
    for index, (guess, _) in enumerate(potential_outcomes.items()):
        pmf[guess] = Decimal(distribution[index])
    return pmf


def _get_counts(potential_outcomes, success_pmf):
    results = {
        'info': {},
        'reward': {},
        'speed': _get_pmf_for_speed(potential_outcomes),
        'minimax': {},
    }
    for guess, possible_responses in potential_outcomes.items():
        reward_pmf = success_pmf(possible_responses)
        results['reward'][guess] = reward_pmf['*']
        entropy_pmf = _get_pmf_for_entropy(possible_responses)
        results['info'][guess] = entropy.get_entropy(entropy_pmf)
        results['minimax'][guess] = entropy.get_inverse_minimax(entropy_pmf)

    return results


def weighted_sum(data, foci):
    normalized_data = {}
    for strategy, strategy_values in data.items():
        total = sum(strategy_values.values())
        normalized_data[strategy] = {k: v/total for k, v in strategy_values.items()}
    guesses = data['info'].keys()
    sums = Counter()
    for guess in guesses:
        for strategy, weight in foci.items():
            strategy_value = normalized_data[strategy][guess]
            if strategy_value == 0.0 and weight == 0.0:
                weighted_value = 0
            else:
                weighted_value = strategy_value*Decimal(weight)
            sums[guess] += weighted_value
    return sums


def weighted_product(data, foci):
    guesses = data['info'].keys()
    products = defaultdict(lambda: 1)
    for guess in guesses:
        for strategy, weight in foci.items():
            strategy_value = data[strategy][guess]
            if strategy_value == 0.0 and weight == 0.0:
                weighted_value = 1
            else:
                weighted_value = strategy_value**Decimal(weight)
            products[guess] *= weighted_value
    return products


def weighted_og(data, foci):
    assert foci == {}, 'The og_weighted model takes no foci'
    guesses = data['info'].keys()
    products = {}
    for guess in guesses:
        products[guess] = data['info'][guess] * data['reward'][guess]
    return products


class Guess(str):
    def __new__(cls, guess, data):
        obj = super().__new__(cls, guess)
        obj.data = data
        return obj


def build_strategy(foci, model=weighted_sum, reward_pmf=None, sorts=[]):

    def strategy(potential_outcomes, game_log):
        data = _get_counts(potential_outcomes, reward_pmf)

        #print('heyo', len(potential_outcomes.all_code_words), sorted(potential_outcomes.all_code_words))

        if len(potential_outcomes.all_code_words) == 1:
            return Guess(list(potential_outcomes.all_code_words)[0], {})

        def reward_sort(guesses, p):
            c = {g: data['reward'][g] for g in guesses if g in data['reward']}
            print(c)
            return c

        sorts = [lexical_sort] # [valid_sort, reward_sort, lexical_sort]

        choices = model(data, foci)
        next_guess = get_actual_next_guess(choices, game_log, sorts, potential_outcomes)
        guess_data = {}
        for strategy, outcomes in data.items():
            guess_data[strategy] = outcomes[next_guess]
        return Guess(next_guess, guess_data)

    return strategy


def lexical_sort(guesses, potential_outcomes):
    return {sorted(guesses)[0]: Decimal(1)}


def random_sort(guesses, potential_outcomes):
    return {random.choice(sorted(guesses)): Decimal(1)}


def valid_sort(guesses, potential_outcomes):
    potential_words = potential_outcomes.all_code_words
    results = {}
    for guess in guesses:
        results[guess] = Decimal(1.0) if guess in potential_words else Decimal(0.0)
    return results


def get_actual_next_guess(choices, game_log, sorts, potential_outcomes):
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

    if len(most_common_guesses) == 1:
        return most_common_guesses[0]

    if len(sorts) >= 1:
        next_sort = sorts.pop(0)
        return get_actual_next_guess(
            next_sort(most_common_guesses, potential_outcomes),
            game_log,
            sorts,
            potential_outcomes
        )
    else:
        result = random.choice(sorted(most_common_guesses))
        return result
