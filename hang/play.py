from hang import opponent, player


class GameLog(list):
    @property
    def guesses(self):
        return {t['guess'] for t in self}


def play(code_word, possible_words, get_potentials, get_next_guess, get_response):
    game_log = GameLog()
    possible_words = list(possible_words)
    while True:
        potentials = get_potentials(possible_words, get_response, game_log)
        next_guess = get_next_guess(potentials, game_log)
        response = get_response(code_word, next_guess)
        game_log.append({
            'guess': next_guess,
            'result': response,
            # 'possible_words': possible_words
        })
        if next_guess == code_word:
            break
        possible_words = potentials.get_by_guess_response(next_guess, response)

    return next_guess, game_log


if __name__ == '__main__':
    from argparse import ArgumentParser
    import fileinput
    import random

    # Seed random so we can do multiple runs with same set of random words
    # TODO: Move this to argument
    random.seed(91514, version=1)

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('--limit', default=1000, type=int)
    args = parser.parse_args()

    words = [word.strip() for word in fileinput.input(args.file)]
    print(len(words))

    if args.limit:
        words = random.sample(words, args.limit)

    games = []
    for word in words:
        game_state, game_log = play(
            word,
            words,
            player.get_potentials,
            player.get_next_guess_naive, opponent.get_response
        )
        assert(game_state == word)
        # print(word, game_state)
        # print(len(game_log))
        games.append(game_log)

    print('Average guesses: ', sum([len(l) for l in games])/len(games))