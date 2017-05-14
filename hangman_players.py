from collections import Counter, OrderedDict
import fractions
import random

import dictionary
import entropy
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
    most_common_letters = []
    most_common_count = None
    for letter, count in _most_common(counts):
        if letter not in game_state.guesses and letter != '*':
            if most_common_count is None:
                most_common_count = count
                most_common_letters.append(letter)
            elif most_common_count == count:
                most_common_letters.append(letter)
            else:
                break
    return random.choice(sorted(most_common_letters))


def entropy_next_guess(game_state, encoded_dictionary):
    """
    Ex:

    counters = {
        #'e': {'e-e': 6, '-ee': 11, 'ee-': 1, 'eee': 2, '*': 107, 'e': 87},
        #'x': {'x': 1, '*': 1},
        #'a': {'--a': 180, 'a--': 5, '*': 185},
        #'b': {'b--': 185, '*': 185}
    }
    total = 185
    """
    rejected_letters = game_state.missed_letters  # Why do we need to pass this in explicitly?
    remaining_words = dictionary.filter_words(encoded_dictionary, game_state, rejected_letters)
    positional_counters = counters.count_positional_letters(remaining_words)
    total = len(remaining_words)
    pmfs = entropy.get_pmfs(positional_counters, total)
    entropies = entropy.get_entropies(pmfs, total)
    scorer = scorers.build_multiplier_scorer(known_multiplier=1.0, missed_multiplier=1.0)

    def utility_function(pmf):
        print(pmf['!'])
        loss = scorer(known_letters=pmf['*'], missed_letters=pmf['!'])
        loss = loss or 0.000001 # Utility should actually be infinity but close enough
        return 1 / loss

    distinct_pmf = {}
    letter_total = positional_counters['*']
    distinct_pmf['!'] = fractions.Fraction(total - letter_total, total)
    for letter, counter in positional_counters.items():
        if letter == '*':
            continue
        distinct_pmf[letter] = fractions.Fraction(counter['*'], total)

    gains = OrderedDict() # entropies with applied gain function
    for letter, letter_entropy in entropies.items():
        pmf = pmfs[letter]
        #print(letter_entropy * utility_function(pmf), float(distinct_counter[letter]))
        gains[letter] = letter_entropy * utility_function(pmf)# * distinct_pmf[letter]

    most_common_letters = []
    most_common_count = None
    for letter, count in _most_common(gains):
        if letter not in game_state.guesses and letter != '*':
            if most_common_count is None:
                most_common_count = count
                most_common_letters.append(letter)
            elif most_common_count == count:
                most_common_letters.append(letter)
            else:
                break
    return random.choice(sorted(most_common_letters))
