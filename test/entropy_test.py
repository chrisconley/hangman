from decimal import Decimal
import random
import unittest

from games import entropy
from hangman_utils import counters


class EntropyTests(unittest.TestCase):
    def assertDecimalAlmostEqual(self, actual, expected, places):
        self.assertEqual(type(actual), Decimal)
        self.assertAlmostEqual(float(actual), expected, places=places)

    def test_max_info_gain(self):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        counts = counters.count_positional_letters(words)
        entropies = entropy.get_new_entropies(counts)

        self.assertDecimalAlmostEqual(entropies['g'], 1.750, places=3)
        self.assertDecimalAlmostEqual(entropies['t'], 1.406, places=3)
        self.assertDecimalAlmostEqual(entropies['a'], 0.811, places=3)
        self.assertDecimalAlmostEqual(entropies['h'], 0.544, places=3)

    def test_log_entropy(self):
        self.assertDecimalAlmostEqual(entropy.log_probability(Decimal(1.0)), 0, places=4)
        self.assertDecimalAlmostEqual(entropy.log_probability(Decimal(0.0)), 0, places=4)
        self.assertDecimalAlmostEqual(entropy.log_probability(Decimal(0.5)), 0.5000, places=4)

        self.assertDecimalAlmostEqual(entropy.log_probability(Decimal(0.01)), 0.0664, places=4)
        self.assertDecimalAlmostEqual(entropy.log_probability(Decimal(0.02)), 0.1129, places=4)

        self.assertDecimalAlmostEqual(entropy.log_probability(Decimal(0.98)), 0.0286, places=4)
        self.assertDecimalAlmostEqual(entropy.log_probability(Decimal(0.99)), 0.0144, places=4)

    def test_get_pmf(self):
        counts = {'ee': 80, 'eee': 2, '*': 10, 'e': 8, '!': 0}
        pmf = entropy.get_pmf(counts)
        self.assertDecimalAlmostEqual(pmf['ee'], 0.80, places=4)
        self.assertDecimalAlmostEqual(pmf['!'], 0.00, places=4)
        self.assertDecimalAlmostEqual(pmf['*'], 0.10, places=4)

        counts = {'ee': 18, 'eee': 2, '*': 107, 'e': 87}
        pmf = entropy.get_pmf(counts)
        self.assertDecimalAlmostEqual(pmf['ee'], 0.08411214953271028, places=17)

    def test_get_entropy(self):
        pmf = {
            'q': Decimal(0.5),
            'b': Decimal(0.125),
            'c': Decimal(0.125),
            'd': Decimal(0.25)
        }
        pmf_entropy = entropy.get_entropy(pmf)
        self.assertDecimalAlmostEqual(pmf_entropy, Decimal('1.75000000000000000'), places=17)

    def test_get_entropy_requires_decimals(self):
        pmf = {
            'q': 0.99,
            'r': 0.01
        }
        with self.assertRaises(AssertionError):
            entropy.get_entropy(pmf)

    def test_get_entropy_requires_pmf_probababilities_add_to_one(self):
        pmf = {
            'q': 1.00,
            'r': 0.01
        }
        with self.assertRaises(AssertionError):
            entropy.get_entropy(pmf)

    def test_get_pmfs_deprecated(self):
        counters = {
            'e': {'ee': 18, 'eee': 2, '*': 107, 'e': 87},
            'x': {'x': 185, '*': 185}
        }
        total = 185
        pmf = entropy.get_pmfs_deprecated(counters, total)
        self.assertAlmostEqual(float(pmf['e']['!']), 0.4216, places=4)
        self.assertAlmostEqual(float(pmf['e']['*']), 0.5784, places=4)
        self.assertAlmostEqual(float(pmf['e']['e']), 0.4703, places=4)
        self.assertAlmostEqual(float(pmf['e']['ee']), 0.0973, places=4)
        self.assertAlmostEqual(float(pmf['e']['eee']), 0.0108, places=4)
        self.assertAlmostEqual(sum([float(p) for p in pmf['e'].values()]), 1.5784, places=4)
        self.assertEqual(pmf['x'], {'!': 0.0, '*': 1.0, 'x': 1.0})

    def test_most_entropy_duplicates(self):
        # TODO: Add '!'
        counters = {
            'e': {'ee': 18, 'eee': 2, '*': 107, 'e': 87},
            'x': {'x': 1, '*': 1},
            'a': {'a': 185, '*': 185}
        }
        total = 185
        pmfs = entropy.get_pmfs_deprecated(counters, total)
        entropies = entropy.get_entropies_deprecated(pmfs, total)
        most_common = entropies.most_common()
        self.assertEqual(most_common[0], ('e', Decimal('1.434861961943034532507727964')))
        self.assertEqual(most_common[1], ('x', Decimal('0.04848740692447229998691670478')))
        self.assertEqual(most_common[2], ('a', Decimal(0.0)))

    def test_most_entropy_positional(self):
        counters = {
            'e': {'e-e': 6, '-ee': 11, 'ee-': 1, 'eee': 2, '*': 107, 'e': 87},
            'x': {'x--': 1, '*': 1},
            'a': {'--a': 180, 'a--': 5, '*': 185},
            'b': {'b--': 185, '*': 185}
        }
        total = 185
        pmfs = entropy.get_pmfs_deprecated(counters, total)
        entropies = entropy.get_entropies_deprecated(pmfs, total)
        most_common = entropies.most_common()
        self.assertEqual(most_common[0][0], 'e')
        self.assertDecimalAlmostEqual(most_common[0][1], 1.551051838789653, places=5)

        self.assertEqual(most_common[1][0], 'a')
        self.assertDecimalAlmostEqual(most_common[1][1], 0.1792560669283215, places=5)

        self.assertEqual(most_common[2][0], 'x')
        self.assertDecimalAlmostEqual(most_common[2][1], 0.04848740692447222, places=5)

        self.assertEqual(most_common[3], ('b', 0.0))

    def test_minimax(self):
        counters = {
            'e': {'e-e': 6, '-ee': 11, 'ee-': 1, 'eee': 2, '*': 107, 'e': 87},
            'a': {'--a': 180, 'a--': 5, '*': 185},
            'b': {'b--': 185, '*': 185}
        }
        minimax = entropy.get_minimax(counters)
        self.assertEqual(minimax, {
            'e': 87,
            'a': 180,
            'b': 185,
        })
