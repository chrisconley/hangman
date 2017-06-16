"""
Takes a input file of words and prints a list of most common letters.

Usage:
$ cat ./games/hangman/words.txt | python -m games.hangman.load_common_letters -
esiarntolcdupmghbyfvkwzxqj
"""

from games import player_utils


def count_distinct_letters(words):
    counter = player_utils.OrderedCounter()
    for word in words:
        for letter in set(word):
            counter[letter] += 1
    return counter

if __name__ == '__main__':
    from argparse import ArgumentParser
    import fileinput

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()

    words = [word.strip() for word in fileinput.input(args.file)]

    counts = count_distinct_letters(words)

    most_common = []
    for letter, count in counts.most_common():
        if args.verbose:
            print(letter, count)
        most_common.append(letter)

    print(''.join(most_common))
