from collections import Counter, defaultdict


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




def get_potential_next_guesses(remaining_words, get_response):
    potentials = {}
    word_guesses = get_unique_guesses(remaining_words)
    for word_guess in word_guesses:
        potentials[word_guess] = defaultdict(set)
        for actual_word in remaining_words:
            response_key = get_response(actual_word, word_guess)
            potentials[word_guess][response_key].add(actual_word)
    return potentials
