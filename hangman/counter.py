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

def learn_word(word, counters={}, thorough=False):
    for length in range(0, len(word)+1):
        word_set = set(word)
        combinations = itertools.combinations(sorted(word_set), length)
        for subset in combinations:

            if thorough:
                key = MysteryString(word, set(subset))
            else:
                key = ''.join(subset)

            counters.setdefault(key, {})

            remaining_letters = word_set.difference(subset)
            if remaining_letters:
                for letter in remaining_letters:
                    counter = counters[key].setdefault(letter, Counter())
                    next_subset = set(subset)
                    next_subset.add(letter)
                    next_key = MysteryString(word, next_subset)
                    counter[next_key] += 1
                    counter['total'] += 1
            #else:
                ## this might not be needed - (if we're doing thorough because if we're here,
                ## it's the word
                #letter = '$'
                #counter = counters[key].setdefault(letter, Counter())
                #next_subset = set(subset)
                #next_subset.add(letter)
                #next_key = MysteryString(word, next_subset)
                #counter[next_key] += 1
                #counter['total'] += 1

            counters[key].setdefault('total', 0)
            counters[key]['total'] += 1
    return counters

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

if __name__ == '__main__':
    import json
    import fileinput
    import sys
    buckets = {}
    for word in fileinput.input():
        word = word.strip()
        length = len(word)
        bucket = buckets.setdefault(length, [])
        bucket.append(word)

    bucket_counts = [len(words) for words in buckets.values()]
    print bucket_counts
    print sum(bucket_counts)

    # We may be able to save time/memory by bucketing into word lengths

    #counters = {}
    #for word in fileinput.input():
        #learn_word(word.strip(), counters, thorough=True)
    #key_size = len(counters)
    #print key_size

    #for key, counts in counters.items():
        #line = json.dumps({'key': key, 'counts': counts})
        #sys.stdout.write("".join([line, '\n']))

    #unittest.main()


