"""
Usage:

time head -n 100 words.txt | python2.7 naive/counter.py - --counter distinct
"""
from collections import Counter

def distinct_generator(word):
    for letter in set(word):
        yield letter

def duplicates_generator(word):
    letter_counter = Counter()
    for letter in word:
        letter_counter[letter] += 1

    for letter, count in letter_counter.items():
        yield letter*count

GENERATORS = {
    'distinct': distinct_generator,
    'duplicates': duplicates_generator
}


if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import json
    import fileinput
    import sys
    import csv

    def GeneratorType(t):
        valid_types = GENERATORS.keys()
        if t not in valid_types:
            message = 'Type must be one of {}'.format(valid_types)
            raise ArgumentTypeError(message)

        return t

    parser = ArgumentParser()
    parser.add_argument('file', help='input dictionary')
    parser.add_argument('--counter', default='distinct', type=GeneratorType)
    args = parser.parse_args()

    counter = Counter()
    for word in fileinput.input(args.file):
        word = word.strip()

        generator = GENERATORS[args.counter]
        for letter in generator(word):
            counter[letter] += 1
        counter['*'] += 1

    writer = csv.writer(sys.stdout)
    for key, count in counter.items():
        writer.writerow([key, count])

