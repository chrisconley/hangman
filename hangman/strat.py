from collections import Counter
import itertools
import re
import unittest

from hangman.game import MysteryString

def learn_word(word, counts={}):
    for length in range(0, len(word)+1):
        word_set = set(word)
        combinations = itertools.combinations(word_set, length)
        for subset in combinations:
            if not len(subset):
                continue
            ms = MysteryString(word, set(subset))

            counter = counts.setdefault(ms, Counter())
            remaining_letters = word_set.difference(subset)
            for letter in remaining_letters:
                counter[letter] += 1
    return counts

#words = ['synth', 'pyscho', 'sites', 'siete']

#for word in words:
    #learn_word(word)

#for k, v in counts.items():
    #print k, v

class Tests(unittest.TestCase):

    def test_duplicate_letters(self):
        counts = learn_word('sites')
        self.assertIsNone(counts.get('s----'))
        self.assertEqual(counts.get('s---s'), Counter({'i': 1, 'e': 1, 't': 1}))

    def test_overlapping_words(self):
        counts = learn_word('synth')
        counts = learn_word('siete')
        expected_counter = Counter({'t': 2, 'e': 1, 'i': 1, 'h': 1, 'n': 1, 'y': 1}) 
        self.assertEqual(counts.get('s----'), expected_counter)

if __name__ == '__main__':
    with open('words-short.txt', 'r') as f:
        counts = {}
        for word in f:
            #print word.strip()
            counts = learn_word(word, counts)
        print len(counts)
    unittest.main()


