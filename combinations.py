import itertools

def positional_combinator(iterable):
    pool = tuple(iterable)
    n = len(pool)
    word_indices = range(n)
    for subset_length in range(n+1):
        for subset in itertools.combinations(word_indices, subset_length):
            t = tuple(pool[i] if i in subset else '-' for i in word_indices)
            yield t

def distinct_combinator(iterable):
    n = len(iterable)
    for subset_length in range(n+1):
        for subset in itertools.combinations(set(iterable), subset_length):
            yield sorted(subset)

def combinator(iterable):
    for combination in positional_combinator(iterable):
        yield tuple(l for l in sorted(combination) if l != '-')

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
def unknown_combinator(iterable):
    word_set = set(iterable)
    alphabet = set(ALPHABET)
    remaining = alphabet.difference(word_set)
    for subset in distinct_combinator(remaining):
        yield sorted(subset)


if __name__ == '__main__':
    count = 0
    for subset in positional_combinator('cathod'):
        #print subset
        count += 1

    for subset in distinct_combinator('cathod'):
        #print subset
        count += 1

    for subset in combinator('cathoda'):
        #print subset
        count += 1

    #unknown_combinator('cathoda')
    for subset in unknown_combinator('cathoda'):
        print subset
        count += 1

    print count
