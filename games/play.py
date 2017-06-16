from games import code_words
from games.mastermind import opponent, player


GUESS_CACHE = {}
REMAINING_WORDS_CACHE = {}


def play(code_word, dictionary, get_potential_outcomes, get_next_guess, get_response, game_log, use_cache=True):
    possible_words = list(dictionary)
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
            potential_outcomes = get_potential_outcomes(possible_words, get_response, game_log)
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
        possible_words = dictionary.bits_to_words(remaining_word_bits)


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

    # words = [word.strip() for word in fileinput.input(args.file)]
    # print(len(words))
    words = opponent.generate_words('ABCDEF', 4)
    print(len(words))

    if args.limit:
        words_to_play = random.sample(words, args.limit)

    games = []
    # words_to_play = ['micrified']
    for word in words_to_play:
        game_state, game_log = play(
            word,
            code_words.Dictionary(words),
            opponent.get_potential_next_guesses,
            player.build_strategy(info_focus=1.0, success_focus=0.0),
            opponent.get_response,
            game_log=opponent.GameLog(),
            use_cache=False
        )
        assert(game_state == word)
        # print(word, game_state)
        # print(len(game_log))
        games.append(game_log)

    print('Average guesses: ', sum([len(l) for l in games])/len(games))
