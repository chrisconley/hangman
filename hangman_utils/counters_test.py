import unittest

from hangman_utils import counters


class WordCounterTests(unittest.TestCase):
    def test_count_distinct_letters(self):
        words = ['cat', 'cot', 'can', 'coto']
        counter = counters.count_distinct_letters(words)
        self.assertEqual(counter['a'], 2)
        self.assertEqual(counter['c'], 4)
        self.assertEqual(counter['n'], 1)
        self.assertEqual(counter['o'], 2)
        self.assertEqual(counter['t'], 3)

    def test_count_duplicate_letters(self):
        words = ['cat', 'cot', 'can', 'coto']
        counter = counters.count_duplicate_letters(words)
        self.assertEqual(counter['a'], {'*': 2, 'a': 2})
        self.assertEqual(counter['c'], {'*': 4, 'c': 4})
        self.assertEqual(counter['n'], {'*': 1, 'n': 1})
        self.assertEqual(counter['o'], {'*': 2, 'o': 1, 'oo': 1})
        self.assertEqual(counter['t'], {'*': 3, 't': 3})

    def test_count_positional_letters(self):
        words = ['cat', 'cot', 'can', 'coto', 'coot']
        counter = counters.count_positional_letters(words)
        self.assertEqual(counter['a'], {'*': 2, '-a-': 2})
        self.assertEqual(counter['c'], {'*': 5, 'c--': 3, 'c---': 2})
        self.assertEqual(counter['n'], {'*': 1, '--n': 1})
        self.assertEqual(counter['o'], {'*': 3, '-o-': 1, '-o-o': 1, '-oo-': 1})
        self.assertEqual(counter['t'], {'*': 4, '--t': 2, '--t-': 1, '---t': 1})
        self.assertEqual(counter['*'], 5)
        self.assertListEqual(sorted(list(counter.keys())), sorted(['*', 'o', 'a', 'c', 'n', 't']))

    def test_count_positional_letters_again(self):
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
        ]
        counter = counters.count_positional_letters(words)
        self.assertEqual(counter['a'], {'*': 6, '---a-----': 6})
        self.assertEqual(counter['t'], {'*': 5, '-t-------': 4, '----t----': 1})
        self.assertEqual(counter['g'], {'*': 4, '------g--': 1, '-----g---': 1, '----gg---': 2})

        self.assertEqual(counter['*'], 8)

    def test_count_positional_letters_for_battleship(self):
        words = ['1100', '1010', '1001', '0110', '0101', '0011']
        counter = counters.count_positional_letters(words)
        self.assertEqual(counter['*'], 6)
        self.assertListEqual(sorted(list(counter.keys())), sorted(['*', '0', '1']))
        self.assertEqual(counter['1'], {
            '*': 6,
            '11--': 1,
            '1-1-': 1,
            '1--1': 1,
            '-11-': 1,
            '-1-1': 1,
            '--11': 1,
        })
        self.assertEqual(counter['0'], {
            '*': 6,
            '--00': 1,
            '-0-0': 1,
            '-00-': 1,
            '0--0': 1,
            '0-0-': 1,
            '00--': 1,
        })
