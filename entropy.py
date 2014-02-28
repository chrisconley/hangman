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

    #print pmfs
    return pmfs

def log_entropy(probability):
    """
    -xlog(x) (base 2)
    """
    if probability == 0.0:
        return 0
    return -probability * math.log(probability, 2)

def get_entropy(probabilities):
    entropy = sum([log_entropy(p) for p in probabilities])
    return entropy

def get_entropies(pmfs, word_count):
    entropies = Counter()
    for letter, pmf in pmfs.items():
        if letter == '*':
            raise Exception('* not allowed')

        probabilities = [p for (subset, p) in pmf.items() if subset != '*']
        if letter == 'i' or letter == 'r':
            print 'probabilities for letter {}'.format(letter), sorted(probabilities)
        s = "{:0.8f}".format(sum(probabilities))
        assert s == '1.00000000', "Probability sum {} does not equal 1.00".format(s)
        entropies[letter] = get_entropy(probabilities)

        # If their is no chance of a miss, we want to make sure we pick it
        # even though in some cases, entropy will be zero
        #if pmf['!'] == 0.0:
            #entropies[letter] += 1000000000
    #print '~~~entropies', entropies

    #for letter, count in entropies.most_common():
        #yield letter, count
    return entropies
