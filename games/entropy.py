# TODO: Rename to math, or optimizations
from decimal import Decimal, getcontext
import fractions
import math

# getcontext().prec = 10

from collections import Counter, OrderedDict


class OrderedCounter(Counter, OrderedDict):
    pass


# TODO: change so last subset makes up difference to 1.0?
# TODO: change to fractions? Then convert to decimal in entropy
# get_pmf asserts that counter values are integers and returns fraction
# get_entropy asserts that values are fractions and returns Decimals
def get_pmf(counter):
    pmf = {}
    total = Decimal(sum(counter.values()))
    for subset, count in counter.items():
        pmf[subset] = Decimal(count) / total
    return pmf


def get_entropy(pmf):
    probabilities = list(pmf.values())
    probabilities_sum = sum(probabilities)
    assert type(probabilities_sum) == Decimal, 'PMF values must be Decimals'
    # assert probabilities_sum == Decimal(1.0), "Probability sum {} does not equal 1.00".format(probabilities_sum)
    entropy = sum([log_probability(p) for p in probabilities])
    return entropy


def get_pmfs_deprecated(counters, total):
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
            # TODO: Get this out of here
            continue
        pmf = pmfs.setdefault(letter, {})
        if counter.get('*'):
            letter_total = counter['*']
            pmf['!'] = Decimal(Decimal(total - letter_total) / Decimal(total))
        for subset, count in counter.items():
            pmf[subset] = Decimal(Decimal(count) / Decimal(total))

    return pmfs


def get_minimax(counters):
    """

    """
    minimax = OrderedCounter()
    for letter, counts in counters.items():
        if letter == '*':
            continue

        minimax[letter] = max([count for subset, count in counts.items() if subset != '*'])
    return minimax


def log_probability(probability):
    """
    -xlog(x) (base 2)
    """
    if probability == 0.0:
        return Decimal(0)
    return -probability * (probability.ln() / Decimal(2.0).ln())


def get_entropy_deprecated(probabilities):
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


def get_entropies_deprecated(pmfs, word_count):
    entropies = OrderedCounter()
    for letter, pmf in pmfs.items():
        if letter == '*':
            raise Exception('* not allowed')

        probabilities = [p for (subset, p) in pmf.items() if subset != '*']
        s = "{:0.8f}".format(float(sum(probabilities)))
        assert s == '1.00000000', "Probability sum {} does not equal 1.00".format(s)
        entropies[letter] = get_entropy_deprecated(probabilities)
    return entropies


def get_new_entropies(counts):
    pmfs = get_pmfs_deprecated(counts, counts['*'])
    return get_entropies_deprecated(pmfs, counts['*'])
