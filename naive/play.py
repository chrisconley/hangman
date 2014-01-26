from collections import Counter
from hangman import game

def strategy(previous_result):
    for letter, count in counter.most_common():
        if letter not in previous_result.guesses and letter != '*':
            return previous_result.guesses | set(letter)

if __name__ == '__main__':
    from argparse import ArgumentParser
    import csv
    import fileinput
    import sys

    with open('/tmp/naive.distinct.csv') as csvfile:
        reader = csv.reader(csvfile)
        counter = Counter()
        for row in reader:
            key = str(row[0])
            count = float(row[1])
            counter[key] = count
    MEMORY = counter

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('--counter', default='distinct')

    args = parser.parse_args()
    total = 0
    for word in fileinput.input(args.file):
        result = game.play(word.strip(), strategy=strategy)
        total += result[2]
    print total
