"""
Usage:

time head -n 100 words.txt | python2.7 naive/counter.py -

# and to count by word length
python2.7 naive/counter.py ./build/splits/5
"""
from collections import Counter

def generator(word):
    for letter in set(word):
        yield letter

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import json
    import fileinput
    import sys
    import csv

    parser = ArgumentParser()
    parser.add_argument('file', help='input dictionary')
    args = parser.parse_args()

    counter = Counter()
    for word in fileinput.input(args.file):
        word = word.strip()

        for letter in generator(word):
            counter[letter] += 1
        counter['*'] += 1

    writer = csv.writer(sys.stdout)
    for key, count in counter.items():
        writer.writerow([key, count])

