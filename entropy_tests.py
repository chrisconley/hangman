import unittest

import entropy

class EntropyTests(unittest.TestCase):
    def test_log_entropy(self):
        self.assertAlmostEqual(entropy.log_entropy(1.0), 0, places=4)
        self.assertAlmostEqual(entropy.log_entropy(0.0), 0, places=4)
        self.assertAlmostEqual(entropy.log_entropy(0.5), 0.5000, places=4)

        self.assertAlmostEqual(entropy.log_entropy(0.01), 0.0664, places=4)
        self.assertAlmostEqual(entropy.log_entropy(0.02), 0.1129, places=4)

        self.assertAlmostEqual(entropy.log_entropy(0.98), 0.0286, places=4)
        self.assertAlmostEqual(entropy.log_entropy(0.99), 0.0144, places=4)

    def test_get_pmf(self):
        counters = {
            'e': {'ee': 18, 'eee': 2, '*': 107, 'e': 87},
            'x': {'x': 185, '*': 185}
        }
        total = 185
        pmf = entropy.get_pmfs(counters, total)
        self.assertAlmostEqual(pmf['e']['!'], 0.4216, places=4)
        self.assertAlmostEqual(pmf['e']['*'], 0.5784, places=4)
        self.assertAlmostEqual(pmf['e']['e'], 0.4703, places=4)
        self.assertAlmostEqual(pmf['e']['ee'], 0.0973, places=4)
        self.assertAlmostEqual(pmf['e']['eee'], 0.0108, places=4)
        self.assertAlmostEqual(sum(pmf['e'].values()), 1.5784, places=4)
        self.assertEqual(pmf['x'], {'!': 0.0, '*': 1.0, 'x': 1.0})

    def test_most_entropy_duplicates(self):
        counters = {
            'e': {'ee': 18, 'eee': 2, '*': 107, 'e': 87},
            'x': {'x': 1, '*': 1},
            'a': {'a': 185, '*': 185}
        }
        total = 185
        pmfs = entropy.get_pmfs(counters, total)
        g = entropy.most_entropy(pmfs, total)
        self.assertEqual(g.next(), ('a', 1000000000))
        self.assertEqual(g.next(), ('e', 1.4348619619430347))
        self.assertEqual(g.next(), ('x', 0.04848740692447222))

    def test_most_entropy_positional(self):
        counters = {
            'e': {'e-e': 6, '-ee': 11, 'ee-': 1, 'eee': 2, '*': 107, 'e': 87},
            'x': {'x': 1, '*': 1},
            'a': {'--a': 180, 'a--': 5, '*': 185},
            'b': {'b--': 185, '*': 185}
        }
        total = 185
        pmfs = entropy.get_pmfs(counters, total)
        g = entropy.most_entropy(pmfs, total)
        self.assertEqual(g.next(), ('a', 1000000000.179256066928))
        self.assertEqual(g.next(), ('b', 1000000000))
        self.assertEqual(g.next(), ('e', 1.551051838789653))
        self.assertEqual(g.next(), ('x', 0.04848740692447222))
