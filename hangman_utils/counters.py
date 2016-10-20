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
