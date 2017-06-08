from collections import Counter, OrderedDict
from decimal import Decimal
import fractions
import random

import dictionary
from hang import entropy
from hangman_utils import counters
import scorers


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


class OrderedCounter(Counter, OrderedDict):
    pass


def _get_last_word(game_state, encoded_dictionary):
    rejected_letters = game_state.missed_letters  # Why do we need to pass this in explicitly?
    remaining_words = dictionary.filter_words(encoded_dictionary, game_state, rejected_letters)
    if len(remaining_words) == 1:
        return remaining_words[0]


def naive(game_state, encoded_dictionary):
    last_word = _get_last_word(game_state, encoded_dictionary)
    if last_word:
        return last_word

    # Generated with `cat words.txt | python load_common_letters.py -`
    letters = 'esiarntolcdupmghbyfvkwzxqj'
    for letter in letters:
        if letter not in game_state.guesses:
            return letter


def _most_common(counter):
    counter = OrderedCounter(counter)
    for letter, count in counter.most_common():
        if letter == '*':
            continue
        yield letter, count


def most_common(game_state, encoded_dictionary):
    rejected_letters = game_state.missed_letters  # Why do we need to pass this in explicitly?
    remaining_words = dictionary.filter_words(encoded_dictionary, game_state, rejected_letters)
    positional_counters = counters.count_positional_letters(remaining_words)
    counts = OrderedCounter()
    for letter, counter in positional_counters.items():
        if letter == '*':
            continue
        counts[letter] = counter['*']
    return get_actual_next_guess(game_state, counts)


def _get_counts(remaining_words):
    counts = counters.count_positional_letters(remaining_words)
    pmfs = entropy.get_pmfs(counts, len(remaining_words))
    common = {letter: pmf['*'] for letter, pmf in pmfs.items()}
    entropies = entropy.get_entropies(pmfs, len(remaining_words))
    results = {}
    if len(remaining_words) <= 26:
        results['remaining_words'] = remaining_words
    results['common'] = common
    results['entropies'] = entropies
    return results


def get_cache_key(game_state):
    current = list(game_state)
    key = "{}:{}".format("".join(current), "".join(sorted(game_state.missed_letters)))
    return key


def build_strategy(info_focus, success_focus, final_word_guess=True, use_cache=False):
    cache = {}
    def strategy(game_state, encoded_dictionary):
        key = get_cache_key(game_state)
        cached_guess = cache.get(key, None)

        if cached_guess and use_cache:
            return cached_guess
        else:
            rejected_letters = game_state.missed_letters  # Why do we need to pass this in explicitly?
            remaining_words = dictionary.filter_words(encoded_dictionary, game_state, rejected_letters)
            data = _get_counts(remaining_words)

            if len(data.get('remaining_words', [])) == 1:
                return data['remaining_words'][0]

            common = data.get('common')
            entropies = data.get('entropies')

            choices = {}
            for letter, pmf in common.items():
                if common[letter] == 0.0 and success_focus == 0.0:
                    common_weight = 1
                else:
                    common_weight = common[letter]**Decimal(success_focus)
                if entropies[letter] == Decimal(0) and info_focus == 0.0:
                    entropy_weight = 1
                else:
                    entropy_weight = entropies[letter]**Decimal(info_focus)
                choices[letter] = entropy_weight * common_weight

            next_guess = get_actual_next_guess(game_state, choices)
            if cached_guess and cached_guess != next_guess:
                raise
                print(key)
                print('cached: ', cached_guess, '|', 'next: ', next_guess)
                print(data)
            cache[key] = next_guess
            return next_guess

    return strategy


def get_actual_next_guess(game_state, choices):
    assert choices.get('*') is None
    most_common_letters = []
    most_common_count = None
    for letter, count in _most_common(choices):
        if letter not in game_state.guesses:
            if most_common_count is None:
                most_common_count = count
                most_common_letters.append(letter)
            elif most_common_count == count:
                most_common_letters.append(letter)
            else:
                break
    if len(most_common_letters) == 0:
        return None
    else:
        return random.choice(sorted(most_common_letters))