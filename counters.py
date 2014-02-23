from collections import Counter
import unittest

def count_distinct_letters(words):
    counter = Counter()
    for word in words:
        for letter in set(word):
            counter[letter] += 1
    return counter

def count_duplicate_letters(words):
    counts = {}
    for word in words:
        for letter in set(word):
            counter = counts.setdefault(letter, Counter())
            key = "".join([l for l in word if l == letter])
            #print word, letter, key
            counter[key] += 1
            counter['*'] += 1
    return counts

def count_positional_letters(words):
    counts = {}
    for word in words:
        for letter in set(word):
            counter = counts.setdefault(letter, Counter())
            key = "".join([l if l == letter else '-' for l in word])
            #print word, letter, key
            counter[key] += 1
            counter['*'] += 1
    return counts

class WordCounterTests(unittest.TestCase):

    def test_count_distinct_letters(self):
        words = ['cat', 'cot', 'can', 'coto']
        counter = count_distinct_letters(words)
        self.assertEqual(counter['a'], 2)
        self.assertEqual(counter['c'], 4)
        self.assertEqual(counter['n'], 1)
        self.assertEqual(counter['o'], 2)
        self.assertEqual(counter['t'], 3)

    def test_count_duplicate_letters(self):
        words = ['cat', 'cot', 'can', 'coto']
        counter = count_duplicate_letters(words)
        self.assertEqual(counter['a'], {'*': 2, 'a': 2})
        self.assertEqual(counter['c'], {'*': 4, 'c': 4})
        self.assertEqual(counter['n'], {'*': 1, 'n': 1})
        self.assertEqual(counter['o'], {'*': 2, 'o': 1, 'oo': 1})
        self.assertEqual(counter['t'], {'*': 3, 't': 3})

    def test_count_positional_letters(self):
        words = ['cat', 'cot', 'can', 'coto', 'coot']
        counter = count_positional_letters(words)
        self.assertEqual(counter['a'], {'*': 2, '-a-': 2})
        self.assertEqual(counter['c'], {'*': 5, 'c--': 3, 'c---': 2})
        self.assertEqual(counter['n'], {'*': 1, '--n': 1})
        self.assertEqual(counter['o'], {'*': 3, '-o-': 1, '-o-o': 1, '-oo-': 1})
        self.assertEqual(counter['t'], {'*': 4, '--t': 2, '--t-': 1, '---t': 1})
