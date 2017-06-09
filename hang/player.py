from collections import Counter, defaultdict, OrderedDict
from decimal import Decimal
import random

from hang import entropy


class OrderedCounter(Counter, OrderedDict):
    pass


def _get_counts(potentials):
    remaining_words = potentials.code_words
    counts = {}
    for guess, responses in potentials.items():
        counts[guess] = OrderedCounter()
        all_words = set()
        for response, words in responses.items():
            counts[guess][response] = len(words)
            if response != '!':
                all_words |= words
        counts[guess]['*'] = len(all_words)
    pmfs = entropy.get_pmfs(counts, len(remaining_words))
    common = {letter: pmf['*'] for letter, pmf in pmfs.items()}
    entropies = entropy.get_entropies(pmfs, len(remaining_words))
    results = {}
    if len(remaining_words) <= 26:
        results['remaining_words'] = remaining_words
    results['common'] = common
    results['entropies'] = entropies
    return results


def build_strategy(info_focus, success_focus, final_word_guess=True, use_cache=False):
    cache = {}

    def strategy(potentials, game_log):
        # key = get_cache_key(game_state)
        cached_guess = False #= cache.get(key, None)

        if cached_guess and use_cache:
            return cached_guess
        else:
            data = _get_counts(potentials)

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

            next_guess = get_actual_next_guess(game_log, choices)
            # cache[key] = next_guess
            return next_guess

    return strategy


def _most_common(counter):
    counter = OrderedCounter(counter)
    for letter, count in counter.most_common():
        if letter == '*':
            continue
        yield letter, count


def get_actual_next_guess(game_log, choices):
    assert choices.get('*') is None
    most_common_letters = []
    most_common_count = None
    for letter, count in _most_common(choices):
        if letter not in game_log.guesses:
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


def get_next_guess_naive(potentials, game_log):
    # If we've whittled down to return one remaining word,
    # return that word as our next guess to finish the game.
    if potentials.total_length == 1:
        return list(potentials.code_words)[0]

    potential_guesses = 'esiarntolcdupmghbyfvkwzxqj'
    worthwhile_guesses = set(''.join(potentials.code_words))
    for guess in potential_guesses:
        if guess in game_log.guesses or guess not in worthwhile_guesses:
            continue
        return guess


class Potential(dict):
    def __init__(self, data={}):
        self._code_words = set()
        super().__init__(self)
        for guess, responses in data.items():
            for response, code_words in responses.items():
                [self.add(guess, response, w) for w in code_words]

    def add(self, guess, response, code_word):
        if self.get(guess) is None:
            self[guess] = defaultdict(set)
        self[guess][response].add(code_word)
        self._code_words.add(code_word)

    def get_by_guess_response(self, guess, response):
        return self[guess][response]

    @property
    def guesses(self):
        return set(self.keys())

    @property
    def total_length(self):
        return len(self._code_words)

    @property
    def code_words(self):
        return self._code_words


def get_potentials(remaining_code_words, get_response, game_log):
    indexed_potentials = Potential()
    potential_guesses = 'esiarntolcdupmghbyfvkwzxqj'
    worthwhile_guesses = set(''.join(remaining_code_words))
    for guess in potential_guesses:
        if guess not in worthwhile_guesses:
            continue
        for code_word in remaining_code_words:
            response = get_response(code_word, guess)
            indexed_potentials.add(guess, response, code_word)
    return indexed_potentials
