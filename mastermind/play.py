import itertools

import hangman_players
from mastermind import opponent, player
from games import entropy


class GameState(str):
    @property
    def guesses(self):
        return []


def play(word, get_next_guess, possible_words):
    game_log = []
    possible_words = list(possible_words)
    while True:
        next_guess, remaining_word_lists = get_next_guess(possible_words, game_log)
        response = opponent.get_response(word, next_guess)
        game_log.append({
            'guess': next_guess,
            'result': response
        })
        if next_guess == word:
            break
        possible_words = remaining_word_lists[response]

    return word, game_log


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

    words = generate_words('ABCDEFG', 4)
    print(len(words))

    if args.limit:
        words = random.sample(words, args.limit)

    games = []
    for word in words:
        game_state, game_log = play(word, get_next_guess, words)
        # print(word, game_state)
        # print(len(game_log))
        games.append(game_log)

    print('Average guesses: ', sum([len(l) for l in games])/len(games))