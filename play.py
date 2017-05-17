import random

import dictionary
import hangman
import hangman_players

if __name__ == '__main__':
    from argparse import ArgumentParser
    import fileinput

    # Seed random so we can do multiple runs with same set of random words
    # TODO: Move this to argument
    random.seed(15243, version=1)

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('--limit', default=1000, type=int)
    args = parser.parse_args()

    words = [word.strip() for word in fileinput.input(args.file)]
    encoded_dictionary = dictionary.encode_dictionary(words)

    if args.limit:
        words = random.sample(words, args.limit)

    # TODO: Add Minimax
    # TODO: Change counts/pmfs to objects, so we don't have '!' and '*' bugs
    # TODO: In game log turn entry, capture expected info gain, minimax, success expectation
    # TODO: In aggregrated game logs, state avg number of turns, max number of turns, (maybe distribution too?)
    games = []
    for word in words:
        game_state, game_log = hangman.play(word, hangman_players.ENTROPY_ONLY, encoded_dictionary)
        # print(word, game_state)
        # print(len(game_log))
        games.append(game_log)

    print(sum([len(l) for l in games])/len(games))