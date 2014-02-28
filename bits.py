from collections import Counter
import random
import unittest

from bitarray import bitarray

import counters
import dictionary
from hangman import game
import entropy


# Initial Knowledge
#naive

# Knowledge at each step
#distinct, duplicate, positional
#use missed letters or not

# Knowledge you'll gain / strategy
#random, most common, distinct letter entropy, duplicate letter entropy, positional letter entropy

def most_common(counter):
    counter = Counter(counter)
    for letter, count in counter.most_common():
        if letter == '*':
            continue
        yield letter, count

def most_common_strategy(mystery_string, counter, total):
    for letter, count in most_common(counter):
        if letter not in mystery_string.guesses and letter != '*':
            return letter

def entropy_strategy(mystery_string, counters, total):

    #counters = {
        #'e': {'e-e': 6, '-ee': 11, 'ee-': 1, 'eee': 2, '*': 107, 'e': 87},
        #'x': {'x': 1, '*': 1},
        #'a': {'--a': 180, 'a--': 5, '*': 185},
        #'b': {'b--': 185, '*': 185}
    #}
    #total = 185
    pmfs = entropy.get_pmfs(counters, total)

    for letter, count in entropy.most_entropy(pmfs, total):
        if letter not in mystery_string.guesses and letter != '*':
            return letter


def get_cache_key(mystery_string, encoder, rejected_letters):

    encoder_keys = {
        'positional': lambda s: list(s),
        'duplicate': lambda s: sorted([key for key in dictionary.duplicate_letters(s)]),
        'distinct': lambda s: sorted([key for key in dictionary.distinct_letters(s)])
    }

    current = encoder_keys[encoder](mystery_string)

    key = "{}:{}".format("".join(current), "".join(sorted(rejected_letters)))

    return key

def get_next_guess(mystery_string, remaining_words, strategy):
    print '@@@@@@@@@@@@@@@@@'
    methods = {
        'entropy-positional': {'counter': counters.count_positional_letters, 'strategy': entropy_strategy},
        'entropy-duplicate': {'counter': counters.count_duplicate_letters, 'strategy': entropy_strategy},
        #'entropy-distinct': {'counter': counters.count_distinct_letters, 'strategy': entropy_strategy},
        # TODO: most-common is best performing right now ?!
        'most-common': {'counter': counters.count_distinct_letters, 'strategy': most_common_strategy},
    }
    counts = methods[strategy]['counter'](remaining_words)
    #print 'counts', counts
    next_guess = methods[strategy]['strategy'](mystery_string, counts, len(remaining_words))
    if len(remaining_words) < 13:
        print remaining_words
    print mystery_string, '|', next_guess, '|', len(remaining_words)#counts
    print '///////////////////'
    return next_guess

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import csv
    import fileinput
    import os.path

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('--encoder', default='positional',
            help='Can be positional, duplicate, distinct or naive')
    parser.add_argument('--track-rejected', dest='track_rejected', action='store_true')
    parser.add_argument('--ignore-rejected', dest='track_rejected', action='store_false')
    parser.add_argument('--strategy', default='entropy-positional',
            help='Can be entropy-positional, entropy-duplicate, entropy-distinct, most-common or random')
    parser.add_argument('--memory-file')
    parser.add_argument('--reset-memory', dest='use_memory', action='store_false')
    parser.add_argument('--limit', default=1000, type=int,
            help='1000 will randomly select 1000 words to play with range')
    parser.add_argument('--range',
            help='1000:2000 will select all words within the range')

    parser.set_defaults(track_rejected=True, use_memory=True)
    args = parser.parse_args()

    words = [word.strip() for word in fileinput.input(args.file)]
    print len(words)
    encoded_dictionary = dictionary.encode_dictionary(words, args.encoder)

    print len(encoded_dictionary.keys())

    print 'playing'
    cached_guesses = {}

    if args.memory_file and os.path.isfile(args.memory_file) and args.use_memory:
        for line in fileinput.input(args.memory_file):
            key, next_guess = line.strip().split(',')
            cached_guesses[key] = next_guess

    words_to_play = words
    if args.range:
        start, stop = args.range.split(':')
        words_to_play = words[int(start):int(stop)]

    if args.limit:
        # Seed random so we can do multiple runs with same set of random words
        random.seed(15243)
        words_to_play = random.sample(words_to_play, args.limit)

    scores = []
    # TODO: introduce word guesses and make scorer count mystery_string.guesses
    # (Basically, we want to normalize the loss function for any kind of guess)
    for word in words_to_play:
        print '###############################'
        print '###############################'
        print '^^^^ {} ^^^^'.format(word)
        print '###############################'
        print '###############################'
        g = game.play(word.strip())
        for mystery_string in g:
            key = get_cache_key(mystery_string, args.encoder, mystery_string.missed_letters)
            next_guess = cached_guesses.get(key, None)
            if not next_guess:
                # TODO: Caching is broken if args.track_rejected is False
                rejected_letters = mystery_string.missed_letters if args.track_rejected else ''
                remaining_words = dictionary.filter_words(encoded_dictionary, mystery_string, rejected_letters)
                if len(remaining_words) == 1:
                    print 'we found it!!!!!!'
                    next_guess = remaining_words[0]
                else:
                    next_guess = get_next_guess(mystery_string, remaining_words, args.strategy)
                cached_guesses[key] = next_guess
            try:
                g.send(next_guess)
            except StopIteration:
                pass
        result = game.MysteryString(word, (set(mystery_string.guesses) | set([next_guess])))
        print word, result, next_guess
        assert word == str(result)

        print word, result.known_letters, result.missed_letters, result.guessed_words
        scores.append(len(result.guesses))

    avg = sum(scores) / float(len(scores))
    print 'Average Score: ', avg

    if args.memory_file:
        with open(args.memory_file, 'w') as memory_file:
            writer = csv.writer(memory_file)
            for key, next_guess in cached_guesses.items():
                writer.writerow([key, next_guess])

