from collections import Counter
import math
from hangman import game

COUNTERS = {}

def most_common(counters):
    word_count = counters['*']
    totals = Counter()
    for letter, counter in counters.items():
        if letter == '*':
            continue
        total = counter['*']
        totals[letter] = total
    for letter, count in totals.most_common():
        yield letter, count

def most_entropy(counters):
    word_count = counters['*']
    entropies = Counter()
    for letter, counter in counters.items():
        if letter == '*':
            continue
        total = counter['*']
        miss_plausibility = float(word_count - total)/float(word_count)
        plausibilities = []
        if miss_plausibility != 0:
            plausibilities.append(miss_plausibility * math.log(miss_plausibility))
            for subset, count in counter.items():
                if subset == '*':
                    continue
                p = float(count) / float(word_count)
                plausibilities.append(p * math.log(p))

            entropy = -1.0 * sum(plausibilities)
            entropies[letter] = entropy
        else: # we know this letter is a match because there are no remaining misses possible
            # This is sorta cheating because entropy should actually be 0
            entropies[letter] = 1000000000
    for letter, count in entropies.most_common():
        yield letter, count

def distinct_key(mystery_string):
    subset = sorted(set([l for l in mystery_string if l in mystery_string.known_letters]))
    key = ''.join(subset)
    return key

def duplicates_key(mystery_string):
    #dupes = sorted([l for l in mystery_string if l != mystery_string.delimiter])
    dupes = sorted([l for l in mystery_string if l in mystery_string.known_letters])
    key = ''.join(dupes)
    return key

def strategy(mystery_string, key_generator, sorter):
    word_length = len(mystery_string)
    key = key_generator(mystery_string)
    counter = COUNTERS[word_length][key]

    for letter, count in sorter(counter):
        if letter not in mystery_string.guesses and letter != '*':
            return mystery_string.guesses | set(letter)

KEYS = {
    'distinct': distinct_key,
    'duplicates': duplicates_key,
}

SORTERS = {
    'most_common': most_common,
    'most_entropy': most_entropy
}

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import csv
    import fileinput
    import json
    import os
    import sys

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('counts', help='counts directory')
    parser.add_argument('--key-generator', default='duplicates')
    parser.add_argument('--sorter', default='most_entropy')
    args = parser.parse_args()

    key_generator = KEYS[args.key_generator]
    sorter = SORTERS[args.sorter]

    dirname = os.path.abspath(args.counts)
    filenames = [
        os.path.join(dirname,f) for f
        in os.listdir(dirname)
        if os.path.isfile(os.path.join(dirname,f))
    ]
    for filename in filenames:
        word_length = int(os.path.basename(filename))
        print filename
        subset_counters = COUNTERS.setdefault(word_length, {})
        with open(filename) as f:
            for line in f:
                data = json.loads(line)
                subset = str(data[0])
                counter = Counter(data[1])
                subset_counters[subset] = counter

    scores = []
    for word in fileinput.input(args.file):
        g = game.play(word.strip(), strategy=strategy)
        result = ''
        for mystery_string in g:
            guesses = strategy(mystery_string, key_generator, sorter)
            try:
                g.send(guesses)
            except StopIteration:
                result = mystery_string
        scores.append(game.default_scorer(result))

    # TODO: hook in univariate to check significance between to methods
    avg = sum(scores) / float(len(scores))
    print avg
