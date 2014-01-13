from collections import Counter
import itertools
import re
import unittest
import hashlib

from hangman.game import MysteryString

LETTER_MAP = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
    'i': 8,
    'j': 9,
    'k': 10,
    'l': 11,
    'm': 12,
    'n': 13,
    'o': 14,
    'p': 15,
    'q': 16,
    'r': 17,
    's': 18,
    't': 19,
    'u': 20,
    'v': 21,
    'w': 22,
    'x': 23,
    'y': 24,
    'z': 25
}

def get_int_hash(key):
    return int(hashlib.md5(key).hexdigest(), 16)

def learn_word(word, counts={}):
    for length in range(0, len(word)+1):
        word_set = set(word)
        combinations = itertools.combinations(word_set, length)
        for subset in combinations:
            if not len(subset):
                continue
            ms = MysteryString(word, set(subset))

            ms_hash = get_int_hash(ms)
            counter = counts.setdefault(ms_hash, [0]*26)
            remaining_letters = word_set.difference(subset)
            for letter in remaining_letters:
                counter[LETTER_MAP[letter]] += 1
    return counts

class Tests(unittest.TestCase):

    def test_duplicate_letters(self):
        counts = learn_word('sites')

        key = get_int_hash('s----')
        self.assertIsNone(counts.get(key))

        key = get_int_hash('s---s')
        expected_counter = [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        self.assertEqual(counts.get(key), expected_counter)

    def test_overlapping_words(self):
        counts = learn_word('synth')
        counts = learn_word('siete')

        key = get_int_hash('s----')
        expected_counter = [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0]
        self.assertEqual(counts.get(key), expected_counter)

if __name__ == '__main__':
    import fileinput
    counts = {}
    for word in fileinput.input():
        learn_word(word.strip(), counts)
    print len(counts)

    unittest.main()


