"""
This file can be used to generate lists of words that match a
given known state for validating search code against a large
data set

Usage:

time cat build/splits/9 | python hangman_utils/check_matching_words.py - --known 'a2,a5,l7,e8' --missed 't'

"""

import unittest


def is_match(word, known_letters, missed_letters):
    """

    Args:
        word: The actual word, ex: 'apple', 'cottage'
        known_letters: A list of letter indices, ex: ['a0', 't3]
        missed_letters: A set of letters, ex: set(['x', 'n'])

    Returns:

    """
    # are any of the missed letters in the word?
    if not missed_letters.isdisjoint(set(word)):
        return False

    # do any of the know letters not match this word?
    for letter_index in known_letters:
        letter = letter_index[0]
        index = int(letter_index[1:])
        if word[int(index)] != letter:
            return False

    return True


class TestCases(unittest.TestCase):
    def test_is_match(self):

        # no known and one matched missed
        result = is_match('apple', [], set(['x']))
        self.assertEqual(result, True)

        # no known and one unmatched missed
        result = is_match('apple', [], set(['a']))
        self.assertEqual(result, False)

        # one matched known and no missed
        result = is_match('apple', ['a0'], set())
        self.assertEqual(result, True)

        # one unmatched known and no missed
        result = is_match('apple', ['c2'], set())
        self.assertEqual(result, False)

        # one matched known and one matched missed
        result = is_match('apple', ['a0'], set(['x']))
        self.assertEqual(result, True)

        # one matched known and one unmatched missed
        result = is_match('apple', ['a0'], set(['p']))
        self.assertEqual(result, False)

        # one unmatched known and one matched missed
        result = is_match('apple', ['c2'], set(['x']))
        self.assertEqual(result, False)

        # one matched known and one matched missed with long word
        result = is_match('appleapples', ['s10'], set(['x']))
        self.assertEqual(result, True)


if __name__ == '__main__':
    from argparse import ArgumentParser
    import fileinput

    parser = ArgumentParser()
    parser.add_argument('dictionary', help='input dictionary')
    parser.add_argument('--known')
    parser.add_argument('--missed')
    args = parser.parse_args()

    known_letters = args.known.strip().split(',')
    missed_letters = set(args.missed.strip().split(','))

    matching_words = []
    for word in fileinput.input(args.dictionary):
        word = word.strip()
        if is_match(word, known_letters, missed_letters):
            matching_words.append(word)
            print(word)
    print(len(matching_words))
