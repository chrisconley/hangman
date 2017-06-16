from collections import Counter, defaultdict
import itertools

from games import code_words


class GameLog(list):
    @property
    def guesses(self):
        return {t['guess'] for t in self}

    def get_cache_key(self):
        return None

GameState = GameLog


def get_response(actual_word, word_guess):
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
    response_key = ''.join(sorted(response))
    return response_key


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


def get_potentials(remaining_words, get_response, game_log):
    indexed_potentials = code_words.PotentialOutcomes()

    word_guesses = get_unique_guesses(remaining_words)
    for word_guess in word_guesses:
        for actual_word in remaining_words:
            response_key = get_response(actual_word, word_guess)
            indexed_potentials.add(word_guess, response_key, actual_word)
    return indexed_potentials
