from collections import Counter, defaultdict
import itertools

from games import code_words


class GameLog(list):
    @property
    def guesses(self):
        return {t['guess'] for t in self}

    def get_cache_key(self):
        if len(self) == 0:
            return 'START'
        key = ':'.join(['{}{}'.format(t['guess'], t['result']) for t in self])
        return key

GameState = GameLog


def get_response(actual_word, word_guess, track_white_responses=False):
    """
    In An Optimal Mastermind (4,7) Strategy and More Results in the Expected Case
    https://arxiv.org/pdf/1305.1010.pdf, the author "double" counts duplicate guesses
    that garner a "white" response.

    Example: The code word is 3632. Let's work out the response for guess 6326:
    6 garners a "white" response
    3 garners a "white" response
    2 garners a "white" response
    6 garners a "white" response again
    This results in a response of 'WWWW'.

    In contrast, if `track_white_responses` is True, this is how the example is worked out:
    6 garners a "white" response
    3 garners a "white" response
    2 garners a "white" response
    6 does not garner a "white" response becuase the "6" in the code word was already "used"
        for the first "6" in the guess
    This results in a response of 'WWW'.

    """
    actual_letters = list(actual_word)
    guess_letters = list(word_guess)
    response = []
    for index, letter in enumerate(guess_letters):
        if letter == actual_word[index]:
            response.append('B')
            actual_letters[index] = '-'
            guess_letters[index] = '-'
    for index, letter in enumerate(guess_letters):
        if letter == '-':
            continue
        if letter in actual_letters:
            response.append('W')
            if track_white_responses:
                actual_letters[actual_letters.index(letter)] = '-'
                guess_letters[index] = '-'
    response_key = ''.join(sorted(response))
    return response_key


def get_response_alternative(actual_word, word_guess):
    return get_response(actual_word, word_guess, track_white_responses=True)


def get_unique_guesses(words):
    uniques = {}
    for word in list(reversed(sorted(words))):
        partition = partition_word(word)
        uniques[partition] = word
    return sorted(uniques.values())


def get_integer_partitions(length):
    answer = set()
    answer.add((length,))
    for x in range(1, length):
        for y in get_integer_partitions(length - x):
            answer.add(tuple(reversed(sorted((x, ) + y))))
    return answer


def partition_word(word):
    seen_letters = {}
    for letter in word:
        if letter in seen_letters:
            seen_letters[letter] += 1
        else:
            seen_letters[letter] = 1
    return tuple(reversed(sorted(seen_letters.values())))


def get_potentials(partial_dictionary, get_response, game_log):
    indexed_potentials = code_words.PotentialOutcomes()

    # We can only use unique guesses the first turn because
    # in later turns we may need to use guesses that we know are incorrect.
    if len(game_log) == 0:
        words = get_unique_guesses(partial_dictionary.as_words)
    else:
        words = partial_dictionary.all_words
        # words = get_unique_guesses(partial_dictionary.as_words)

    for word_guess in words:
        for actual_word in partial_dictionary.as_words:
            response_key = get_response(actual_word, word_guess)
            indexed_potentials.add(word_guess, response_key, actual_word)
    return indexed_potentials
