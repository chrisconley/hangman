from collections import Counter, OrderedDict
import fractions
import math
import random
import unittest

import counters


class OrderedCounter(Counter, OrderedDict):
    pass


def get_pmfs(counters, total):
    """
    Takes a counter and returns a probability mass function in the form of

    Arguments:

    counter - {'a': {'*': 25, 'a': 21, 'aa': 4}}

    Returns:

    {
        'a': {'!': 0.34, '*': 0.45, 'a': 0.34, 'aa': 0.32}
    }

    NB: Not sure if we want to keep * around
    """
    pmfs = OrderedDict()
    for letter, counter in counters.items():
        if letter == '*':
            continue
        pmf = pmfs.setdefault(letter, {})
        letter_total = counter['*']
        pmf['!'] = fractions.Fraction(total - letter_total, total)
        for subset, count in counter.items():
            pmf[subset] = fractions.Fraction(count, total)

    return pmfs


def log_probability(probability):
    """
    -xlog(x) (base 2)
    """
    if probability == 0.0:
        return 0
    return -probability * math.log(probability, 2)


def get_entropy(probabilities):
    entropy = sum([log_probability(p) for p in probabilities])
    return entropy


def get_square_loss(probabilities):
    return sum([(1 - p*p)**2 for p in probabilities])


def get_hinge_loss(probabilities):
    maximum = max([(1 - p*p)**2 for p in probabilities])
    if maximum < 0.0:
        return 0.0
    else:
        return maximum


def get_entropies(pmfs, word_count):
    entropies = OrderedCounter()
    for letter, pmf in pmfs.items():
        if letter == '*':
            raise Exception('* not allowed')

        probabilities = [p for (subset, p) in pmf.items() if subset != '*']
        s = "{:0.8f}".format(float(sum(probabilities)))
        assert s == '1.00000000', "Probability sum {} does not equal 1.00".format(s)
        entropies[letter] = get_entropy(probabilities)
    return entropies


def get_new_entropies(counts):
    pmfs = get_pmfs(counts, counts['*'])
    return get_entropies(pmfs, counts['*'])


class EntropyTests(unittest.TestCase):

    def test_max_info_gain(self):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        counts = counters.count_positional_letters(words)
        entropies = get_new_entropies(counts)

        self.assertAlmostEqual(entropies['g'], 1.750, places=3)
        self.assertAlmostEqual(entropies['t'], 1.406, places=3)
        self.assertAlmostEqual(entropies['a'], 0.811, places=3)
        self.assertAlmostEqual(entropies['h'], 0.544, places=3)
