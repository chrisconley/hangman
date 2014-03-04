from collections import Counter
import math

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
    pmfs = {}
    for letter, counter in counters.items():
        if letter == '*':
            raise Exception('* not allowed')
        pmf = pmfs.setdefault(letter, {})
        letter_total = counter['*']
        pmf['!'] = (total - letter_total) / float(total)
        for subset, count in counter.items():
            pmf[subset] = count / float(total)

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

def get_entropies(pmfs, word_count):
    entropies = Counter()
    for letter, pmf in pmfs.items():
        if letter == '*':
            raise Exception('* not allowed')

        probabilities = [p for (subset, p) in pmf.items() if subset != '*']
        s = "{:0.8f}".format(sum(probabilities))
        assert s == '1.00000000', "Probability sum {} does not equal 1.00".format(s)
        entropies[letter] = get_entropy(probabilities)

    return entropies
