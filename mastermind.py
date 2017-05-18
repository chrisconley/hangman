import itertools

import hangman_players
from hangman_utils import counters
import entropy


class GameState(str):
    @property
    def guesses(self):
        return []


def generate_words(symbols, length):
    tuples = itertools.product(symbols, repeat=length)
    return sorted(map(lambda t: ''.join(t), tuples))


def play(word, get_next_guess, possible_words):
    game_log = []
    possible_words = list(possible_words)
    while True:
        next_guess, remaining_word_lists = get_next_guess(possible_words)
        response = counters.get_response(word, next_guess)
        game_log.append({
            'guess': next_guess,
            'result': response
        })
        if next_guess == word:
            break
        possible_words = remaining_word_lists[response]

    return word, game_log


def get_next_guess(possible_words):
    next_words = counters.get_potential_next_guesses(possible_words)
    next_guess = _get_next_guess(next_words, len(possible_words))
    return next_guess, next_words.get(next_guess)


def _get_next_guess(next_words, total_remaining_words):
    counts = {}
    for next_guess, next_guess_potentials in next_words.items():
        counts[next_guess] = {}
        for next_response, potentials in next_guess_potentials.items():
            counts[next_guess][next_response] = len(potentials)
    pmfs = entropy.get_pmfs(counts, total_remaining_words)
    entropies = entropy.get_entropies(pmfs, total_remaining_words)

    return hangman_players.get_actual_next_guess(GameState(), entropies)

if __name__ == '__main__':
    from argparse import ArgumentParser
    # import fileinput
    import random

    # Seed random so we can do multiple runs with same set of random words
    # TODO: Move this to argument
    random.seed(154333, version=1)

    parser = ArgumentParser()
    # parser.add_argument('file', help='input words')
    parser.add_argument('--limit', default=1000, type=int)
    args = parser.parse_args()

    words = generate_words('ABCDEF', 4)

    if args.limit:
        words = random.sample(words, args.limit)

    games = []
    for word in words:
        game_state, game_log = play(word, get_next_guess, words)
        # print(word, game_state)
        # print(len(game_log))
        games.append(game_log)

    print('Average guesses: ', sum([len(l) for l in games])/len(games))