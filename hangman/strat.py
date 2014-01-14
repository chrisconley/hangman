"""
Usage:

time head -n 5000 words.txt | python2.7 hangman/strat.py
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
        combinations = itertools.combinations(word_set, length)
        for subset in combinations:
            if not len(subset):
                continue

            if thorough:
                key = MysteryString(word, set(subset))
            else:
                key = ''.join(subset)

            remaining_letters = word_set.difference(subset)
            for letter in remaining_letters:
                letter_key = "{}:{}".format(key, letter)
                counts[letter_key] += 1
    return counts

class Tests(unittest.TestCase):
    def test_non_thorough(self):
        counts = Counter()
        counts = learn_word('sites', counts=counts, thorough=False)
        counts = learn_word('synth', counts=counts, thorough=False)
        counts = learn_word('siete', counts=counts, thorough=False)

        self.assertIsNone(counts.get('ss:t'))

        self.assertIsNone(counts.get('s:a'))
        self.assertEqual(counts.get('s:e'), 2)
        self.assertEqual(counts.get('s:h'), 1)
        self.assertEqual(counts.get('s:i'), 2)
        self.assertEqual(counts.get('s:t'), 3)


    def test_duplicate_letters(self):
        counts = learn_word('sites', Counter(), thorough=True)

        self.assertIsNone(counts.get('s----:t'))

        self.assertIsNone(counts.get('s---s:a'))
        self.assertEqual(counts.get('s---s:t'), 1)

    def test_overlapping_words(self):
        counts = Counter()
        counts = learn_word('synth', counts=counts, thorough=True)
        counts = learn_word('siete', counts=counts, thorough=True)

        self.assertIsNone(counts.get('s----:a'))
        self.assertEqual(counts.get('s----:e'), 1)
        self.assertEqual(counts.get('s----:t'), 2)

def batch_learn(words, counts, thorough=False):
    for word in words:
        learn_word(word, counts, thorough)
    return counts

def callback(something):
    #print something
    pass

if __name__ == '__main__':
    import fileinput
    counts = Counter()
    words = []
    for word in fileinput.input():
        words.append(word.strip())
        #learn_word(word.strip(), counts)
    key_size = len(counts)
    print key_size

    from multiprocessing import Pool, Manager
    pool = Pool(processes=2)
    counts1 = Counter()
    counts2 = Counter()
    length = len(words)
    half = int(length / 2.0)
    results1 = pool.apply_async(batch_learn, [words[0:half], counts1], {}, callback)
    results2 = pool.apply_async(batch_learn, [words[half:-1], counts2])
    #pool.close()
    #pool.join()
    print len(results1.get())
    counts1 = results1.get()
    counts2 = results2.get()
    counts = counts1 + counts2
    print 'async: ', len(counts)

    unittest.main()


