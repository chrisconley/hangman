from collections import Counter
from hangman import game

def distinct_strategy(previous_result):
    for letter, count in counter.most_common():
        if letter not in previous_result.guesses and letter != '*':
            return previous_result.guesses | set(letter)

def duplicates_strategy(previous_result):
    for letter, count in counter.most_common():
        if "".join(set(letter)) not in previous_result.guesses and letter != '*':
            return previous_result.guesses | set(letter)

STRATEGIES = {
    'distinct': distinct_strategy,
    'duplicates': duplicates_strategy
}

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import csv
    import fileinput
    import os
    import sys

    def StrategyType(t):
        valid_types = STRATEGIES.keys()
        if t not in valid_types:
            message = 'Type must be one of {}'.format(valid_types)
            raise ArgumentTypeError(message)
        return t

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('counts', help='counts file')
    parser.add_argument('--strategy', type=StrategyType, default='distinct')
    args = parser.parse_args()

    filename = os.path.abspath(args.counts)
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        counter = Counter()
        for row in reader:
            key = str(row[0])
            count = float(row[1])
            counter[key] = count
    MEMORY = counter


    strategy = STRATEGIES[args.strategy]
    total = 0
    for word in fileinput.input(args.file):
        result = game.play(word.strip(), strategy=strategy)
        total += result[2]
    print total
