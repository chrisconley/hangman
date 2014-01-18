"""
Usage:

time head -n 5000 words.txt | python2.7 hangman/strat.py > hangman/distinct_letter_counts.csv
"""
from collections import Counter
import itertools
import re
import unittest

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

def learn_word(word, counts={}, thorough=False):
    for length in range(0, len(word)+1):
        word_set = set(word)
        combinations = itertools.combinations(sorted(word_set), length)
        for subset in combinations:
            #print subset
            #if not len(subset):
                #continue

            if thorough:
                key = MysteryString(word, set(subset))
            else:
                key = ''.join(subset)

            remaining_letters = word_set.difference(subset)
            if remaining_letters:
                for letter in remaining_letters:
                    letter_key = "{}:{}".format(key, letter)
                    if counts.get(letter_key):
                        counts[letter_key] += 1
                    else:
                        counts[letter_key] = 1
            else:
                letter_key = ":".join([key, "$"])
                if counts.get(letter_key):
                    counts[letter_key] += 1
                else:
                    counts[letter_key] = 1
    return counts

class Tests(unittest.TestCase):
    def test_non_thorough(self):
        counts = {}
        counts = learn_word('sites', counts=counts, thorough=False)
        counts = learn_word('synth', counts=counts, thorough=False)
        counts = learn_word('siete', counts=counts, thorough=False)

        self.assertIsNone(counts.get('ss:t'))

        self.assertIsNone(counts.get('s:a'))
        self.assertEqual(counts.get('s:e'), 2)
        self.assertEqual(counts.get('s:h'), 1)
        self.assertEqual(counts.get('s:i'), 2)
        self.assertEqual(counts.get('s:t'), 3)
        self.assertEqual(counts.get('hnsty:$'), 1)


    def test_duplicate_letters(self):
        counts = learn_word('sites', thorough=True)

        self.assertIsNone(counts.get('s----:t'))

        self.assertIsNone(counts.get('s---s:a'))
        self.assertEqual(counts.get('s---s:t'), 1)

    def test_overlapping_words(self):
        counts = {}
        counts = learn_word('synth', counts=counts, thorough=True)
        counts = learn_word('siete', counts=counts, thorough=True)

        self.assertIsNone(counts.get('s----:a'))
        self.assertEqual(counts.get('s----:e'), 1)
        self.assertEqual(counts.get('s----:t'), 2)

if __name__ == '__main__':
    #import csv
    #import fileinput
    #import sys
    #counts = {}
    #for word in fileinput.input():
        #learn_word(word.strip(), counts)
    #key_size = len(counts)
    ##print key_size

    #writer = csv.writer(sys.stdout)
    #for key, count in counts.items():
        #writer.writerow([key, count])

    unittest.main()


