#!/usr/bin/env python
"""
Hangman:
cat ./build/splits/9 | ./games/play.py - --game hangman --limit 10

Mastermind:
./games/mastermind/word_generator.py ABCDEF:4 | ./games/play.py - --game hangman --limit 1
"""
from collections import defaultdict
from decimal import Decimal
from fractions import Fraction

from games import code_words, player_utils, entropy
from games.player_utils import Guess, OrderedCounter, get_actual_next_guess#, weighted_product
from games.mastermind.opponent import get_unique_guesses
from games.mastermind.player import _get_pmf_for_success


GUESS_CACHE = {}
RESPONSE_CACHE = {}


def get_potential_outcomes(partial_dictionary, get_response, game_log):
    indexed_potentials = code_words.PotentialOutcomes()

    # We can only use unique guesses the first turn because
    # in later turns we may need to use guesses that we know are incorrect.
    # if len(game_log) == 0:
    #     words = get_unique_guesses(partial_dictionary.as_words)
    # else:
    #     words = partial_dictionary.all_words #third option of .as_words
    #words = get_unique_guesses(partial_dictionary.as_words)
    #words = partial_dictionary.as_words
    words = partial_dictionary.all_words
    for word_guess in words:
        for actual_word in partial_dictionary.as_words:
            response_key = get_response(actual_word, word_guess)
            indexed_potentials.add(word_guess, response_key, actual_word)
    return indexed_potentials


def _get_pmf_for_entropy(possible_responses):
    counter = OrderedCounter()
    seen_words = set()
    for response, code_words in possible_responses.items():
        assert code_words.isdisjoint(seen_words), 'There should not be duplicate code words across responses'
        seen_words |= code_words
        counter[response] = len(code_words)
    return entropy.get_pmf(counter)


def _get_counts(potential_outcomes, success_pmf):
    results = {
        'info': {},
        'reward': {},
        'minimax': {},
    }
    for guess, possible_responses in potential_outcomes.items():
        reward_pmf = success_pmf(possible_responses)
        results['reward'][guess] = reward_pmf['*']
        entropy_pmf = _get_pmf_for_entropy(possible_responses)
        # print(entropy_pmf)
        results['info'][guess] = entropy.get_entropy(entropy_pmf)
        results['minimax'][guess] = entropy.get_inverse_minimax(entropy_pmf)

    return results


def get_next_guess(potential_outcomes, game_log):
    # if len(game_log) == 0:
    #     return '1234'

    foci = {
        'info': 1.0,
        'minimax': 0.0,
    }
    data = _get_counts(potential_outcomes, _get_pmf_for_success)

    if len(potential_outcomes.all_code_words) == 1:
        return Guess(list(potential_outcomes.all_code_words)[0], {})

    def weighted_product(data, foci):
        guesses = data['info'].keys()
        products = defaultdict(lambda: 1)
        for guess in guesses:
            strategy_value = data['info'][guess]
            products[guess] = strategy_value
        return products

    choices = weighted_product(data, foci)

    def sort_by_reward(guesses):
        c = {g: data['reward'][g] for g in guesses if g in data['reward']}
        return get_actual_next_guess(c, game_log)

    if True:
        sort_function = lambda guesses: sorted(guesses)[0]
    else:
        sort_function = sort_by_reward

    next_guess = get_actual_next_guess(choices, game_log, sort_function)
    guess_data = {}
    for strategy, outcomes in data.items():
        guess_data[strategy] = outcomes[next_guess]
    return Guess(next_guess, guess_data)


def play(code_word, dictionary, get_response, game_log, use_cache=True):
    partial_dictionary = dictionary.get_partial_dictionary(set(dictionary))
    while True:
        if use_cache:
            cache_key = game_log.get_cache_key()
            if cache_key:
                next_guess, possible_responses = GUESS_CACHE.get(cache_key, (None, None))
            else:
                next_guess, possible_responses, cache_key = None, None, None
        else:
            next_guess, possible_responses, cache_key = None, None, None
        if next_guess is None:
            potential_outcomes = get_potential_outcomes(partial_dictionary, get_response, game_log)
            next_guess = get_next_guess(potential_outcomes, game_log)
            if next_guess != code_word:
                possible_responses = {response: dictionary.words_to_bits(words) for response, words in potential_outcomes[next_guess].items()}
                GUESS_CACHE[cache_key] = (next_guess, possible_responses)


        response = get_response(code_word, next_guess)

        game_log.append({
            'guess': next_guess,
            'result': response,
        })
        if next_guess == code_word:
            break

        remaining_word_bits = possible_responses[response]
        words = dictionary.bits_to_words(remaining_word_bits)
        partial_dictionary = dictionary.get_partial_dictionary(words)

    return next_guess, game_log


def game_log_as_json(game, game_log, seed):
    log_json = []
    for entry in game_log:
        log_json.append({
            'guess': [entry['guess'], {k: float(v) for k,v in entry['guess'].data.items()}],

            'result': entry['result']
        })

    result = {
        'game': game,
        'seed': seed,
        'log': log_json
    }
    return result


class RIS(object):
    def __init__(self, model, foci):
        self.model_string = model
        self.model = getattr(player_utils, model)
        self.foci = foci

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import argparse
    import fileinput
    import json
    import random
    import sys

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('--game')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--seed', type=int)
    parser.add_argument('--outfile', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    words = [word.strip() for word in fileinput.input(args.file)]
    print(len(words), file=sys.stderr)

    # Seed random so we can do multiple runs with same set of random words
    if args.seed:
        random.seed(args.seed, version=1)

    words_to_play = words
    if args.limit:
        words_to_play = random.sample(words, args.limit)
    # else:
    #     words_to_play = random.sample(words, len(words))

    name = 'games.{}.opponent'.format(args.game)
    opponent = __import__(name, fromlist=[''])
    name = 'games.{}.player'.format(args.game)
    player = __import__(name, fromlist=[''])


    # TODO: In game log turn entry, capture expected info gain, minimax, success expectation
    # TODO: In aggregrated game logs, state avg number of turns, max number of turns, (maybe distribution too?)
    games = []
    saved = defaultdict(set)
    for word in words_to_play:
        game_state, game_log = play(
            word,
            code_words.Dictionary(words),
            opponent.get_response,
            game_log=opponent.GameLog(),
            # use_cache=False,
        )
        assert(game_state == word)
        games.append(game_log)
        print(json.dumps(game_log_as_json(
            args.game,
            game_log,
            args.seed
        )), file=args.outfile)
        print(','.join([word, str(len(game_log))]), file=args.outfile)

    print('Total Games: ', len(games), file=sys.stderr)
    print('Average guesses: ', sum([len(l) for l in games])/len(games), file=sys.stderr)
    print('Total guesses: ', sum([len(l) for l in games]), file=sys.stderr)
    print('Max guesses: ', max([len(l) for l in games]), file=sys.stderr)
    print('Min guesses: ', min([len(l) for l in games]), file=sys.stderr)

