#!/usr/bin/env python
"""
Hangman:
cat ./build/splits/9 | ./games/play.py - --game hangman --limit 10

Mastermind:
./games/mastermind/word_generator.py ABCDEF:4 | ./games/play.py - --game hangman --limit 1
"""
from games import code_words, player_utils


GUESS_CACHE = {}
RESPONSE_CACHE = {}


def play(code_word, dictionary, get_potential_outcomes, get_next_guess, get_response, game_log, use_cache=True):
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


def game_log_as_json(game, strategy, game_log, seed):
    log_json = []
    for entry in game_log:
        log_json.append({
            'guess': [entry['guess'], {k: float(v) for k,v in entry['guess'].data.items()}],

            'result': entry['result']
        })

    result = {
        'game': game,
        'seed': seed,
        'strategy': {
            'model': strategy.model_string,
            'foci': strategy.foci
        },
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

    def _ris_strategy(string):
        """
        Ex: "weighted_sum|info:80;reward:10;speed:10"
        """
        model, string = string.split('|')
        splits = string.split(';')
        foci = {}
        the_sum = 0
        for split in splits:
            focus, amount = split.split(':')
            foci[focus] = int(amount) / 100.0
            the_sum += int(amount)
        if the_sum != 100:
            message = 'strategy must add to 100'
            raise ArgumentTypeError(message)
        return RIS(model, foci)

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('--game')
    parser.add_argument('--limit', default=1000, type=int)
    parser.add_argument('--strategy', type=_ris_strategy)
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

    name = 'games.{}.opponent'.format(args.game)
    opponent = __import__(name, fromlist=[''])
    name = 'games.{}.player'.format(args.game)
    player = __import__(name, fromlist=[''])


    # TODO: In game log turn entry, capture expected info gain, minimax, success expectation
    # TODO: In aggregrated game logs, state avg number of turns, max number of turns, (maybe distribution too?)
    games = []
    for word in words_to_play:
        game_state, game_log = play(
            word,
            code_words.Dictionary(words),
            opponent.get_potentials,
            #player.build_knuth_strategy(),
            player.build_strategy(args.strategy.foci, args.strategy.model, sorts=[player_utils.valid_sort, player_utils.lexical_sort]),
            opponent.get_response,
            game_log=opponent.GameLog()
        )
        assert(game_state == word)
        games.append(game_log)
        # print(json.dumps(game_log_as_json(
        #     args.game,
        #     args.strategy,
        #     game_log,
        #     args.seed
        # )), file=args.outfile)

    print('Total Games: ', len(games), file=sys.stderr)
    print('Total guesses: ', sum([len(l) for l in games]), file=sys.stderr)
    print('Average guesses: ', sum([len(l) for l in games])/len(games), file=sys.stderr)
    print('Average incorrect guesses: ', sum([len([True for t in l if t['result'] == '!']) for l in games]) / len(games), file=sys.stderr)
    print('Max guesses: ', max([len(l) for l in games]), file=sys.stderr)
    print('Max guesses: ', max([len(l) for l in games]), file=sys.stderr)

