import random

import dictionary
import hangman
import hangman_players

if __name__ == '__main__':
    from argparse import ArgumentParser
    import fileinput

    # Seed random so we can do multiple runs with same set of random words
    # TODO: Move this to argument
    random.seed(1543, version=1)

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('--limit', default=1000, type=int)
    args = parser.parse_args()

    words = [word.strip() for word in fileinput.input(args.file)]
    encoded_dictionary = dictionary.encode_dictionary(words)

    if args.limit:
        words_to_play = random.sample(words, args.limit)

    foci = [
        (0.25, 0.0),
        (1.0, 0.0),
        (0.75, 0.25),
        (0.5, 0.5),
        (0.25, 0.75),
        (0.0, 1.0),
        (0.0, 0.25)
    ]
    for info_focus, success_focus in foci:
        random.seed(15443, version=1)
        # TODO: Add Minimax
        # TODO: Change counts/pmfs to objects, so we don't have '!' and '*' bugs
        # TODO: In game log turn entry, capture expected info gain, minimax, success expectation
        # TODO: In aggregrated game logs, state avg number of turns, max number of turns, (maybe distribution too?)
        games = []
        hangman_players.CACHE = {}
        strategy = hangman_players.build_strategy(info_focus, success_focus)
        for word in words_to_play:
            game_state, game_log = hangman.play(word, strategy, encoded_dictionary)
            # print(word, game_state)
            # print(len(game_log))
            games.append(game_log)
        print('info: ', info_focus, '|', 'success: ', success_focus)
        print(sum([len(l) for l in games])/len(games))
