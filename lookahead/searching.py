from collections import Counter
import math
from hangman import game

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import csv
    import fileinput
    import json
    import os
    import sys

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    args = parser.parse_args()

    for word in fileinput.input(args.file):
        word = word.strip()
        if set('aben').issubset(set(word)):
            print word, "".join(sorted(word))
