from collections import Counter
from hangman import game

COUNTER = Counter()

def strategy(previous_result):
    for letter, count in COUNTER.most_common():
        if letter not in previous_result.guesses and letter != '*':
            return previous_result.guesses | set(letter)

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import csv
    import fileinput
    import os
    import sys

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('counts', help='counts file')
    args = parser.parse_args()

    filename = os.path.abspath(args.counts)
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key = str(row[0])
            count = float(row[1])
            COUNTER[key] = count

    scores = []
    for word in fileinput.input(args.file):
        result = game.play(word.strip(), strategy=strategy)
        scores.append(result[2])

    avg = sum(scores) / float(len(scores))
    print avg
