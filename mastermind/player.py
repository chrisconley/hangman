from collections import Counter, defaultdict

from mastermind import opponent


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


def count_mastermind_letters(words):
    return count_mastermind_letters_brute(words, get_unique_guesses(words))


def count_mastermind_letters_brute(words, word_guesses=None):
    counts = defaultdict(Counter)
    counts['*'] = 0
    if word_guesses is None:
        word_guesses = words
    for word_guess in word_guesses:
        for actual_word in words:
            response_key = opponent.get_response(actual_word, word_guess)
            counter = counts[word_guess]
            counter['*'] += 1
            counter[response_key] += 1
        counts['*'] += 1
    return counts


def get_potential_next_guesses(remaining_words, get_response):
    potentials = {}
    word_guesses = get_unique_guesses(remaining_words)
    for word_guess in word_guesses:
        potentials[word_guess] = defaultdict(set)
        for actual_word in remaining_words:
            response_key = get_response(actual_word, word_guess)
            potentials[word_guess][response_key].add(actual_word)
    return potentials
