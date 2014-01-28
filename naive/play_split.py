from collections import Counter
from hangman import game

COUNTER = {}

def strategy(previous_result):
    word_length = len(previous_result)
    for letter, count in COUNTER[word_length].most_common():
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
    parser.add_argument('counts', help='counts directory')
    args = parser.parse_args()

    dirname = os.path.abspath(args.counts)
    filenames = [
        os.path.join(dirname,f) for f
        in os.listdir(dirname)
        if os.path.isfile(os.path.join(dirname,f))
    ]
    for filename in filenames:
        word_length = int(os.path.basename(filename))
        counter = COUNTER.setdefault(word_length, Counter())
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                key = str(row[0])
                count = float(row[1])
                counter[key] = count

    scores = []
    for word in fileinput.input(args.file):
        result = game.play(word.strip(), strategy=strategy)
        scores.append(result[2])

    avg = sum(scores) / float(len(scores))
    print avg
