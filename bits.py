from collections import Counter
import random

from bitarray import bitarray

import counters
import dictionary
import entropy
import hangman
from scorers import build_multiplier_scorer

"""
Usage:

time cat build/splits/9 | python2.7 bits.py - --track-rejected --reset-memory --strategy entropy-positional --limit 500
"""


# Initial Knowledge
#naive

# Knowledge at each step
#distinct, duplicate, positional
#use missed letters or not

# Knowledge you'll gain / strategy
#random, most common, distinct letter entropy, duplicate letter entropy, positional letter entropy

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def random_strategy(mystery_string, counter, total, scorer):
    letters = list(ALPHABET)
    random.shuffle(letters)
    for letter in letters:
        if letter not in mystery_string.guesses and letter != '*':
            return letter

def naive_strategy(mystery_string, counter, total, scorer):
    # TODO: get rid of hard coding this
    letters = 'esirantolcdugmphbyfvkwzxqj'
    for letter in letters:
        if letter not in mystery_string.guesses and letter != '*':
            return letter

def most_common(counter):
    counter = Counter(counter)
    for letter, count in counter.most_common():
        if letter == '*':
            continue
        yield letter, count

def most_common_strategy(mystery_string, counter, total, scorer):
    for letter, count in most_common(counter):
        if letter not in mystery_string.guesses and letter != '*':
            return letter


def entropy_strategy(mystery_string, counters, total, scorer):
    """
    Ex:

    counters = {
        #'e': {'e-e': 6, '-ee': 11, 'ee-': 1, 'eee': 2, '*': 107, 'e': 87},
        #'x': {'x': 1, '*': 1},
        #'a': {'--a': 180, 'a--': 5, '*': 185},
        #'b': {'b--': 185, '*': 185}
    }
    total = 185
    """
    pmfs = entropy.get_pmfs(counters, total)
    entropies = entropy.get_entropies(pmfs, total)

    def utility_function(pmf):
        loss = scorer(known_letters=pmf['*'], missed_letters=pmf['!'])
        loss = loss or 0.000001 # Utility should actually be infinity but close enough
        return 1 / loss

    gains = {} # entropies with applied gain function
    for letter, letter_entropy in entropies.items():
        pmf = pmfs[letter]
        gains[letter] = letter_entropy * utility_function(pmf)

    for letter, count in most_common(gains):
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

def get_next_guess(mystery_string, remaining_words, strategy, scorer):
    if len(remaining_words) == 1:
        next_guess = remaining_words[0]
    else:
        methods = {
            'entropy-positional': {'counter': counters.count_positional_letters, 'strategy': entropy_strategy},
            'entropy-duplicate': {'counter': counters.count_duplicate_letters, 'strategy': entropy_strategy},
            #'entropy-distinct': {'counter': counters.count_distinct_letters, 'strategy': entropy_strategy},
            'most-common': {'counter': counters.count_distinct_letters, 'strategy': most_common_strategy},
            'random': {'counter': counters.count_distinct_letters, 'strategy': random_strategy},
            'naive': {'counter': counters.count_distinct_letters, 'strategy': naive_strategy},
        }
        counts = methods[strategy]['counter'](remaining_words)
        strategy_method = methods[strategy]['strategy']
        next_guess = strategy_method(mystery_string, counts, len(remaining_words), scorer)

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
    parser.add_argument('--scorer',
            help='multipler:2:7 - multiplier is the only available score atm')

    parser.set_defaults(track_rejected=True, use_memory=True)
    args = parser.parse_args()

    words = [word.strip() for word in fileinput.input(args.file)]
    encoded_dictionary = dictionary.encode_dictionary(words, args.encoder)

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

    if args.scorer:
        scorer_type, known_multiplier, missed_multiplier = args.scorer.split(':')
        assert scorer_type == 'multiplier'
        scorer = build_multiplier_scorer(float(known_multiplier), float(missed_multiplier))
    else:
        scorer = build_multiplier_scorer(known_multiplier=1.0, missed_multiplier=1.0)
    scores = []
    for word in words_to_play:

        game = hangman.play(word.strip())
        for mystery_string in game:
            key = get_cache_key(mystery_string, args.encoder, mystery_string.missed_letters)
            next_guess = cached_guesses.get(key, None)
            if not next_guess:
                # TODO: Caching is broken if args.track_rejected is False
                rejected_letters = mystery_string.missed_letters if args.track_rejected else ''
                remaining_words = dictionary.filter_words(encoded_dictionary, mystery_string, rejected_letters)
                next_guess = get_next_guess(mystery_string, remaining_words, args.strategy, scorer)
                cached_guesses[key] = next_guess
            try:
                game.send(next_guess)
            except StopIteration:
                pass
        result = hangman.MysteryString(word, (set(mystery_string.guesses) | set([next_guess])))
        assert word == str(result)

        print word, result.known_letters, result.missed_letters, result.guessed_words
        scores.append(scorer(known_letters=len(result.known_letters), missed_letters=len(result.missed_letters)))

    avg = sum(scores) / float(len(scores))
    print 'Average Score: ', avg

    if args.memory_file:
        with open(args.memory_file, 'w') as memory_file:
            writer = csv.writer(memory_file)
            for key, next_guess in cached_guesses.items():
                writer.writerow([key, next_guess])

    # For determining most common letters
    #totals = counters.count_distinct_letters(words)
    #most_common = []
    #for letter, count in Counter(totals).most_common():
        #print letter, count
        #most_common.append(letter)

    #print ''.join(most_common)
    
