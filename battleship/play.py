import itertools

from battleship import opponent, player


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
        if next_guess is None:
            break
        possible_words = remaining_word_lists

    return word, game_log
