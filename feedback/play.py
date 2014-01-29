from collections import Counter
from hangman import game

COUNTERS = {}

def strategy(previous_result):
    word_length = len(previous_result)
    counter = COUNTERS[word_length][''.join(sorted(previous_result.known_letters))]
    for letter, count in counter.most_common():
        if letter not in previous_result.guesses and letter != '*':
            return previous_result.guesses | set(letter)

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
    parser.add_argument('--strategy', default='distinct')
    args = parser.parse_args()

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
