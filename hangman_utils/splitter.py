"""
Usage"

head words.txt | python ./hangman_utils/splitter.py - ./build/splits
python ./hangman_utils/splitter.py ./hangman_utils/words.txt ./build/splits
"""

if __name__ == '__main__':
    from argparse import ArgumentParser
    import fileinput
    import os
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

    lengths= [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28]

    for length in lengths:
        filename = os.path.abspath(os.path.join(args.destination, str(length)))
        with open(filename, 'w') as f:
            for word in buckets.get(length, []):
                f.write('{}\n'.format(word))
