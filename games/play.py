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


class RIS(object):
    def __init__(self, model, foci):
        self.model = getattr(player_utils, model)
        self.foci = foci

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import fileinput
    import random
    import sys

    def _ris_strategy(string):
        """
        Ex: "weighted_sum|info:80;reward:10;speed:10"
        """
        model, string = string.split('|')
        splits = string.split(';')
        foci = {}
        for split in splits:
            focus, amount = split.split(':')
            foci[focus] = int(amount) / 100.0
        if sum(foci.values()) != 1.0:
            message = 'strategy must add to 100'
            raise ArgumentTypeError(message)
        return RIS(model, foci)

    # Seed random so we can do multiple runs with same set of random words
    # TODO: Move this to argument
    random.seed(91514, version=1)

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('--game')
    parser.add_argument('--limit', default=1000, type=int)
    parser.add_argument('--strategy', type=_ris_strategy)
    args = parser.parse_args()

    words = [word.strip() for word in fileinput.input(args.file)]
    print(len(words))

    word_to_play = words
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
            player.build_strategy(args.strategy.foci, args.strategy.model),
            opponent.get_response,
            game_log=opponent.GameLog()
        )
        assert(game_state == word)
        games.append(game_log)
        for turn in game_log:
            print(turn['guess'], turn['guess'].data)

    print('Average guesses: ', sum([len(l) for l in games])/len(games))
    def _count_wrongs(log):
        return len([turn for turn in log if turn['result'] == '!'])
    print('Average wrong guesses: ', sum(_count_wrongs(log) for log in games) / len(games))
    print('Max guesses: ', max([len(l) for l in games]))

