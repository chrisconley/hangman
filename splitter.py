"""
Usage"

head words.txt | python2.7 ./splitter.py - ./build/splits
python2.7 ./splitter.py ./words.txt ./build/splits
"""

if __name__ == '__main__':
    from argparse import ArgumentParser
    import json
    import fileinput
    import os
    import sys
    import csv
    parser = ArgumentParser()
    parser.add_argument('dictionary', help='input dictionary')
    parser.add_argument('destination', help='destination directory to dump the dictionary splits to')
    args = parser.parse_args()

    buckets = {}
    for word in fileinput.input(args.dictionary):
        word = word.strip()
        length = len(word)
        buckets.setdefault(length, [])
        buckets[length].append(word)

    for length, words in buckets.items():
        filename = os.path.abspath(os.path.join(args.destination, str(length)))
        with open(filename, 'w') as f:
            for word in words:
                f.write('{}\n'.format(word))
