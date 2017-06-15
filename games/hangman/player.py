from collections import Counter, defaultdict, OrderedDict
from decimal import Decimal, getcontext
import random

from games import entropy


# getcontext().prec = 10


class OrderedCounter(Counter, OrderedDict):
    pass


def _get_pmf_for_success(possible_responses):
    counter = OrderedCounter()
    successful_code_words = set()
    seen_words = set()
    for response, code_words in possible_responses.items():
        assert code_words.isdisjoint(seen_words), 'There should not be duplicate code words across responses'
        seen_words |= code_words
        if response == '!':
            counter['!'] = Decimal(len(code_words))
        else:
            successful_code_words |= code_words
    counter['*'] = Decimal(len(successful_code_words))
    return entropy.get_pmf(counter)


def _get_pmf_for_entropy(possible_responses):
    counter = OrderedCounter()
    seen_words = set()
    for response, code_words in possible_responses.items():
        assert code_words.isdisjoint(seen_words), 'There should not be duplicate code words across responses'
        seen_words |= code_words
        counter[response] = Decimal(len(code_words))
    return entropy.get_pmf(counter)


def _get_counts(potential_outcomes):
    common = {}
    entropies = {}
    for guess, possible_responses in potential_outcomes.items():
        common_pmf = _get_pmf_for_success(possible_responses)
        common[guess] = common_pmf['*']
        entropy_pmf = _get_pmf_for_entropy(possible_responses)
        entropies[guess] = entropy.get_entropy(entropy_pmf)

    results = {}
    results['common'] = common
    results['entropies'] = entropies
    return results


def _get_cache_key(game_log):
    hidden_word = []
    missed_guesses = set()
    for entry in game_log:
        if entry['result'] == '!':
            missed_guesses.add(entry['guess'])
        else:
            if hidden_word == []:
                hidden_word = list(entry['result'])
            else:
                for index, character in enumerate(entry['result']):
                    if character == '-':
                        continue
                    hidden_word[index] = character
    key = "{}:{}".format("".join(hidden_word), "".join(sorted(missed_guesses)))
    return key


def build_strategy(info_focus, success_focus, final_word_guess=True, use_cache=False):
    cache = {}

    def strategy(potential_outcomes, game_log):
        key = _get_cache_key(game_log)
        cached_guess = cache.get(key, None)

        if cached_guess and use_cache:
            return cached_guess
        else:
            data = _get_counts(potential_outcomes)

            if len(potential_outcomes.all_code_words) == 1:
                return list(potential_outcomes.all_code_words)[0]

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
            cache[key] = next_guess
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
        return list(potentials.all_code_words)[0]

    potential_guesses = 'esiarntolcdupmghbyfvkwzxqj'
    worthwhile_guesses = set(''.join(potentials.all_code_words))
    for guess in potential_guesses:
        if guess in game_log.guesses or guess not in worthwhile_guesses:
            continue
        return guess
