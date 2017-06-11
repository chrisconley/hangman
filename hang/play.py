import opponent, player
import dictionary
import code_words


class GameLog(list):
    @property
    def guesses(self):
        return {t['guess'] for t in self}


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

GUESS_CACHE = {}
REMAINING_WORDS_CACHE = {}


def play(code_word, dictionary, get_potential_outcomes, get_next_guess, get_response):
    game_log = GameLog()
    possible_words = list(dictionary)
    while True:
        cache_key = _get_cache_key(game_log)
        next_guess, possible_responses = GUESS_CACHE.get(cache_key, (None, None))
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

    words = [word.strip() for word in fileinput.input(args.file)]
    print(len(words))

    if args.limit:
        words_to_play = random.sample(words, args.limit)

    games = []
    # words_to_play = ['micrified']
    for word in words_to_play:
        game_state, game_log = play(
            word,
            code_words.Dictionary(words),
            player.get_potentials,
            player.build_strategy(info_focus=1.0, success_focus=0.0, final_word_guess=True, use_cache=True),
            opponent.get_response
        )
        assert(game_state == word)
        # print(word, game_state)
        # print(len(game_log))
        games.append(game_log)

    print('Average guesses: ', sum([len(l) for l in games])/len(games))
