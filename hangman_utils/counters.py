from collections import Counter, defaultdict, OrderedDict


class OrderedCounter(Counter, OrderedDict):
    pass


def count_distinct_letters(words):
    counter = OrderedCounter()
    for word in words:
        for letter in set(word):
            counter[letter] += 1
    return counter


def count_duplicate_letters(words):
    counts = OrderedCounter()
    for word in words:
        for letter in set(word):
            counter = counts.setdefault(letter, OrderedCounter())
            key = "".join([l for l in word if l == letter])

            counter[key] += 1
            counter['*'] += 1
    return counts


def count_positional_letters(words):
    counts = defaultdict(OrderedCounter)
    counts['*'] = 0
    for word in words:
        for letter in set(word):
            counter = counts[letter]
            key = "".join([l if l == letter else '-' for l in word])
            counter[key] += 1
            counter['*'] += 1
        counts['*'] += 1
    return counts


def count_index_letters(words):
    counts = defaultdict(OrderedCounter)
    counts['*'] = 0
    for word in words:
        for index, letter in enumerate(word):
            counter = counts[str(index)]
            counter[letter] += 1
            counter['*'] += 1
        counts['*'] += 1
    return counts


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
    counts = defaultdict(OrderedCounter)
    counts['*'] = 0
    if word_guesses is None:
        word_guesses = words
    for word_guess in word_guesses:
        for actual_word in words:
            response_key = get_response(actual_word, word_guess)
            counter = counts[word_guess]
            counter['*'] += 1
            counter[response_key] += 1
        counts['*'] += 1
    return counts


def get_potential_next_guesses(remaining_words):
    potentials = {}
    word_guesses = get_unique_guesses(remaining_words)
    for word_guess in word_guesses:
        potentials[word_guess] = defaultdict(set)
        for actual_word in remaining_words:
            response_key = get_response(actual_word, word_guess)
            potentials[word_guess][response_key].add(actual_word)
    return potentials


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
