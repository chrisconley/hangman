"""
Usage:

time head -n 5000 words.txt | python2.7 hangman/strat.py > hangman/distinct_letter_counts.csv
"""
from collections import Counter
import itertools
import re
import unittest

import redis
REDIS = redis.StrictRedis(host='localhost', port=6379, db=12)

from hangman.game import MysteryString

---, c--, -a-, --t, ca-, c-t, -at, cat

def learn_word(word, counter):
    pipe = REDIS.pipeline()
    for length in range(0, len(word)+1):
        word_set = set(word)
        combinations = itertools.combinations(sorted(word_set), length)
        for subset in combinations:

            key = str(MysteryString(word, set(subset)))

            remaining_letters = word_set.difference(subset)
            if remaining_letters:
                for letter in remaining_letters:
                    next_subset = set(subset)
                    next_subset.add(letter)
                    next_key = str(MysteryString(word, next_subset))
                    redis_key = ":".join([key, letter])
                    pipe.hincrby(redis_key, next_key, 1)
                    pipe.hincrby(redis_key, 'total', 1)

            total_key = ":".join([key, 'total'])
            pipe.incrby(total_key, 1)
    pipe.execute()
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
    buckets = {}
    for word in fileinput.input():
        word = word.strip()
        length = len(word)
        bucket = buckets.setdefault(length, [])
        bucket.append(word)

    #bucket_counts = [len(words) for words in buckets.values()]
    #print bucket_counts
    #print sum(bucket_counts)


    #rand_obj = random.choice(objgraph.by_type('set'))
    #objgraph.show_chain(objgraph.find_backref_chain(rand_obj,inspect.ismodule),filename='chain.png')

    # We may be able to save time/memory by bucketing into word lengths

    REDIS.flushdb()
    for word_length, words in buckets.items():
        counter = Counter()
        for word in words:
            learn_word(word.strip(), counter)
        key_size = len(counter)
        print 'key_size'
        print key_size

        writer = csv.writer(sys.stdout)
        for key, count in counter.items():
            writer.writerow([key, count])

    #unittest.main()


