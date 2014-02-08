from collections import Counter
import math
from hangman import game

COUNTERS = {}

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

def duplicates_strategy(previous_result):
    word_length = len(previous_result)
    key = ''.join(sorted([l for l in previous_result if l in previous_result.known_letters]))
    counter = COUNTERS[word_length][key]

    # TODO: choose max entropy instead of most_common
    for letter, count in most_entropy(counter):
        if letter not in previous_result.guesses and letter != '*':
            return previous_result.guesses | set(letter)

STRATEGIES = {
    'duplicates': duplicates_strategy,
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
    parser.add_argument('--strategy', default='duplicates')
    args = parser.parse_args()

    strategy = STRATEGIES[args.strategy]

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
        result = game.play(word.strip(), strategy=strategy)
        scores.append(result[2])

    # TODO: hook in univariate to check significance between to methods
    avg = sum(scores) / float(len(scores))
    print avg
