from collections import Counter
import itertools
import re
import unittest

from hangman.game import MysteryString

def learn_word(word, counts={}):
    for length in range(0, len(word)+1):
        combinations = itertools.combinations(word, length)
        for subset in combinations:
            ms = MysteryString(word, set(subset))


            # if our matched letters don't match our current subset,
            # then move to the next subset.
            #
            # Ex:
            #
            # For the word 'sites', we will see ('s',) and ('s','s')
            # as subsets, but we only want to continue on with ('s', 's')
            # because our only valid MysteryString is 's---s'.
            if tuple(re.sub('-', '', ms)) != subset:
                continue

            counter = counts.setdefault(ms, Counter())
            for letter in set(word):
                if letter not in subset and len(subset):
                    if ms == 's---s':
                        print subset, letter
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

    def test_duplicate_letters(self):
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


