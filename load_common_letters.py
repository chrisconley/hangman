"""
Takes a input file of words and prints a list of most common letters.

Usage:
$ cat words.txt | python load_common_letters.py -
esiarntolcdupmghbyfvkwzxqj
"""
import counters

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import fileinput

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()

    words = [word.strip() for word in fileinput.input(args.file)]

    counts = counters.count_distinct_letters(words)

    most_common = []
    for letter, count in counts.most_common():
        if args.verbose:
            print(letter, count)
        most_common.append(letter)

    print(''.join(most_common))
