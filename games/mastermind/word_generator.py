#!/usr/bin/env python
"""
Usage

This will generate words for commercialized version of Mastermind.
./games/mastermind/word_generator.py ABCDEF:4
"""

import argparse
import itertools
import sys


def generate_words(symbols, length):
    tuples = itertools.product(symbols, repeat=length)
    return sorted(map(lambda t: ''.join(t), tuples))


def main(args):
    symbols, length = args.dictionary.split(':')
    for word in generate_words(symbols, int(length)):
        print(word)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dictionary')
    parser.add_argument('--output-file', type=argparse.FileType('r'), default=sys.stdout)
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())
