from collections import Counter
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

def strategy(mystery_string, counter):
    for letter, count in most_common(counter):
        if letter not in mystery_string.guesses and letter != '*':
            return mystery_string.guesses | set(letter)

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

def other_scorer(result):
    if len(result.missed_words) >= 5:
        return 25
    else:
        return (len(result.guesses) * 1) + (len(result.missed_words) * 1)


def get_cache_key(mystery_string, encoder, rejected_letters):

    encoder_keys = {
        'positional': lambda s: list(s),
        'duplicate': lambda s: sorted([key for key in dictionary.duplicate_letters(s)]),
        'distinct': lambda s: sorted([key for key in dictionary.distinct_letters(s)])
    }

    current = encoder_keys[encoder](mystery_string)

    key = "{}:{}".format("".join(current), "".join(sorted(rejected_letters)))

    return key

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import csv
    import fileinput
    import os.path

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    parser.add_argument('--encoder', default='positional')
    parser.add_argument('--track-rejected', dest='track_rejected', action='store_true')
    parser.add_argument('--ignore-rejected', dest='track_rejected', action='store_false')
    parser.add_argument('--strategy', default='entropy-positional')
    parser.add_argument('--memory-file')

    parser.set_defaults(track_rejected=True)
    args = parser.parse_args()

    words = [word.strip() for word in fileinput.input(args.file)]
    print len(words)
    encoded_dictionary = dictionary.encode_dictionary(words, args.encoder)

    #for key, a in encoded_dictionary.items():
        #print key, a
    print len(encoded_dictionary.keys())

    print 'playing'
    cached_guesses = {}

    if os.path.isfile(args.memory_file):
        for line in fileinput.input(args.memory_file):
            key, next_guess = line.strip().split(',')
            cached_guesses[key] = next_guess

    scores = []
    other_scores = []
    for word in words[8000:9000]:
        g = game.play(word.strip(), strategy=strategy)
        result = ''
        for mystery_string in g:
            key = get_cache_key(mystery_string, args.encoder, mystery_string.missed_letters)
            next_guess = cached_guesses.get(key, None)
            if not next_guess:
                # TODO: Caching is broken if args.track_rejected is False
                rejected_letters = mystery_string.missed_letters if args.track_rejected else ''
                remaining_words = dictionary.filter_words(encoded_dictionary, mystery_string, rejected_letters)
                # TODO: Have this determined by args.strategy
                counts = counters.count_duplicate_letters(remaining_words)
                next_guess = entropy_strategy(mystery_string, counts, len(remaining_words))
                cached_guesses[key] = next_guess
            try:
                g.send(next_guess)
            except StopIteration:
                result = mystery_string

        print word, mystery_string.known_letters, mystery_string.missed_letters
        scores.append(game.default_scorer(result))
        other_scores.append(other_scorer(result))

    avg = sum(scores) / float(len(scores))
    other_avg = sum(other_scores) / float(len(other_scores))
    print 'Average Score: ', avg
    print 'Average Other Score: ', other_avg

    with open(args.memory_file, 'w') as memory_file:
        writer = csv.writer(memory_file)
        for key, next_guess in cached_guesses.items():
            writer.writerow([key, next_guess])

