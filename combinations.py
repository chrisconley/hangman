import itertools

def combi(iterable):
    pool = tuple(iterable)
    n = len(pool)
    word_indices = range(n)
    for subset_length in range(n+1):
        for subset in itertools.combinations(word_indices, subset_length):
            t = tuple(pool[i] if i in subset else '-' for i in word_indices)
            yield t

if __name__ == '__main__':
    for subset in combi('cathod'):
        print subset

