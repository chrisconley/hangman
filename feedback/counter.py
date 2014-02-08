from collections import Counter
import itertools

def distinct_generator(iterable):
    word_set = set(iterable)
    n = len(iterable)
    for subset_length in range(n+1):
        for subset in itertools.combinations(set(iterable), subset_length):
            remaining_letters = word_set.difference(subset)
            subset = sorted(subset)
            if remaining_letters:
                yield subset, remaining_letters

def duplicates_generator(iterable):
    for combination, remaining_letters in distinct_generator(iterable):
        subset = set(combination)
        yield tuple(l for l in sorted(iterable) if l in subset), remaining_letters

def ordered_generator(iterable):
    for combination, remaining_letters in distinct_generator(iterable):
        subset = set(combination)
        yield tuple(l for l in iterable if l in subset), remaining_letters

def positional_generator(iterable):
    for combination, remaining_letters in distinct_generator(iterable):
        subset = set(combination)
        yield tuple(l if l in subset else '-' for l in iterable), remaining_letters


GENERATORS = {
    'distinct': distinct_generator,
    'duplicates': duplicates_generator,
    'ordered': ordered_generator,
    'positional': positional_generator
}

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import json
    import fileinput
    import sys
    import csv

    def GeneratorType(t):
        valid_types = GENERATORS.keys()
        if t not in valid_types:
            message = 'Type must be one of {}'.format(valid_types)
            raise ArgumentTypeError(message)
        return t

    parser = ArgumentParser()
    parser.add_argument('file', help='input dictionary')
    parser.add_argument('--counter', default='distinct', type=GeneratorType)
    args = parser.parse_args()

    counters = {}
    for word in fileinput.input(args.file):
        word = word.strip()

        generator = GENERATORS[args.counter]
        for subset, remaining_letters in generator(word):
            counter = counters.setdefault(''.join(subset), Counter())
            counter['*'] += 1
            for letter in remaining_letters:
                counter[letter] += 1

    for key, counter in counters.items():
        sys.stdout.write("{}\n".format(json.dumps([key, counter])))
