"""
Usage:

time head -n 5000 words.txt | python2.7 hangman/strat.py > hangman/distinct_letter_counts.csv
"""
from collections import Counter
import itertools
import re
import unittest

from hangman.game import MysteryString

from combinations import combinator, distinct_combinator, positional_combinator


def learn_word(word, counter):
    for subset in distinct_combinator(word):
        counter["".join(subset)] += 1
    return counter

class Tests(unittest.TestCase):
    def test_overlapping_words(self):
        counters = {}
        counters = learn_word('sites', counters=counters, thorough=True)
        counters = learn_word('synth', counters=counters, thorough=True)
        counters = learn_word('siete', counters=counters, thorough=True)

        self.assertEqual(counters.get('s--t-'), {
            'total': 2,
            'e': Counter({'total': 1, 's-ete': 1}),
            'i': Counter({'total': 1, 'si-t-': 1}),
            'y': Counter({'total': 1, 'sy-t-': 1}),
            'n': Counter({'total': 1, 's-nt-': 1}),
            'h': Counter({'total': 1, 's--th': 1}),
        })

    def test_duplicate_letters(self):
        counters = learn_word('sites', thorough=True)

        self.assertIsNone(counters.get('s----'))

        self.assertIsNone(counters['s---s'].get('a'))
        self.assertEqual(counters.get('s---s'), {
            'total': 1,
            'e': Counter({'total': 1, 's--es': 1}),
            'i': Counter({'total': 1, 'si--s': 1}),
            't': Counter({'total': 1, 's-t-s': 1}),
        })

import sys
def show_sizeof(x, level=0):
    print "\t" * level, x.__class__, sys.getsizeof(x), x
    if hasattr(x, '__iter__'):
        if hasattr(x, 'items'):
            for xx in x.items():
                show_sizeof(xx, level + 1)
        else:
            for xx in x:
                show_sizeof(xx, level + 1)

if __name__ == '__main__':
    import json
    import fileinput
    import sys
    import csv
    counter = Counter()
    for word in fileinput.input():
        learn_word(word.strip(), counter)

    writer = csv.writer(sys.stdout)
    for key, count in counter.items():
        writer.writerow([key, count])

    #unittest.main()


