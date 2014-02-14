from collections import Counter
import math

def log_entropy(probability):
    """
    -xlog(x) (base 2)
    """
    if probability == 0.0:
        return 0
    return -probability * math.log(probability, 2)

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

def get_entropy(probabilities):
    entropy = sum([log_entropy(p) for p in probabilities])
    return entropy

def most_entropy(pmfs, word_count):
    entropies = Counter()
    for letter, counter in pmfs.items():
        if letter == '*':
            raise Exception('* not allowed')

        pmf = pmfs[letter]
        if pmf['!'] != 0.0:
            probabilities = [p for (subset, p) in pmf.items() if subset != '*']
            entropies[letter] = get_entropy(probabilities)
        else: # we know this letter is a match because there are no remaining misses possible
            # This is sorta cheating because entropy should actually be 0
            entropies[letter] = 1000000000
    for letter, count in entropies.most_common():
        yield letter, count
