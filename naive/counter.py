"""
Usage:

time head -n 100 words.txt | python2.7 naive/counter.py - --counter distinct
"""
from collections import Counter

if __name__ == '__main__':
    from argparse import ArgumentParser
    import json
    import fileinput
    import sys
    import csv
    parser = ArgumentParser()
    parser.add_argument('file', help='input dictionary')
    parser.add_argument('--counter', default='distinct')
    args = parser.parse_args()

    counter = Counter()
    for word in fileinput.input(args.file):
        word = word.strip()
        for letter in set(word):
            counter[letter] += 1
        counter['*'] += 1

    writer = csv.writer(sys.stdout)
    for key, count in counter.items():
        writer.writerow([key, count])

