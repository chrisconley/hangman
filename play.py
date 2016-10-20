import fractions
import random
import unittest
from collections import Counter, OrderedDict

import dictionary
import entropy
import hangman
from hangman_utils import counters
from scorers import build_multiplier_scorer

"""
Usage:

time cat build/splits/9 | python play.py - --reset-memory --strategy entropy-positional --limit 500
"""

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def random_strategy(game_state, positional_counters, total, scorer):
    letters = list(ALPHABET)
    random.shuffle(letters)
    for letter in letters:
        if letter not in game_state.guesses and letter != '*':
            return letter

def naive_strategy(game_state, positional_counters, total, scorer):
    # Generated with `cat words.txt | python load_common_letters.py -`
    letters = 'esiarntolcdupmghbyfvkwzxqj'
    for letter in letters:
        if letter not in game_state.guesses and letter != '*':
            return letter

class OrderedCounter(Counter, OrderedDict):
    pass

def most_common(counter):
    counter = OrderedCounter(counter)
    for letter, count in counter.most_common():
        if letter == '*':
            continue
        yield letter, count


def most_common_strategy(game_state, positional_counters, total, scorer):
    counts = OrderedCounter()
    for letter, counter in positional_counters.items():
        if letter == '*':
            continue
        counts[letter] = counter['*']
    most_common_letters = []
    most_common_count = None
    for letter, count in most_common(counts):
        if letter not in game_state.guesses and letter != '*':
            if most_common_count is None:
                most_common_count = count
                most_common_letters.append(letter)
            elif most_common_count == count:
                most_common_letters.append(letter)
            else:
                break
    return random.choice(sorted(most_common_letters))


def get_actual_next_guess(game_state, choices):
    assert choices.get('*') is None
    most_common_letters = []
    most_common_count = None
    for letter, count in most_common(choices):
        if letter not in game_state.guesses:
            if most_common_count is None:
                most_common_count = count
                most_common_letters.append(letter)
            elif most_common_count == count:
                most_common_letters.append(letter)
            else:
                break
    return random.choice(sorted(most_common_letters))


def entropy_strategy(game_state, positional_counters, total, scorer):
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
    pmfs = entropy.get_pmfs(positional_counters, total)
    entropies = entropy.get_entropies(pmfs, total)

    def utility_function(pmf):
        loss = scorer(known_letters=pmf['*'], missed_letters=pmf['!'])
        loss = loss or 0.000001 # Utility should actually be infinity but close enough
        return 1 / loss

    distinct_pmf = {}
    letter_total = positional_counters['*']
    distinct_pmf['!'] = fractions.Fraction(total - letter_total, total)
    for letter, counter in positional_counters.items():
        if letter == '*':
            continue
        distinct_pmf[letter] = fractions.Fraction(counter['*'], total)

    gains = OrderedDict() # entropies with applied gain function
    for letter, letter_entropy in entropies.items():
        pmf = pmfs[letter]
        #print(letter_entropy * utility_function(pmf), float(distinct_counter[letter]))
        gains[letter] = letter_entropy * utility_function(pmf)# * distinct_pmf[letter]

    most_common_letters = []
    most_common_count = None
    for letter, count in most_common(gains):
        if letter not in game_state.guesses and letter != '*':
            if most_common_count is None:
                most_common_count = count
                most_common_letters.append(letter)
            elif most_common_count == count:
                most_common_letters.append(letter)
            else:
                break
    return random.choice(sorted(most_common_letters))


def get_cache_key(game_state, rejected_letters):
    current = list(game_state)
    key = "{}:{}".format("".join(current), "".join(sorted(rejected_letters)))
    return key


def get_next_guess(game_state, remaining_words, strategy, scorer):
    if len(remaining_words) == 1:
        next_guess = remaining_words[0]
    else:
        methods = {
            'entropy-positional': {'strategy': entropy_strategy},
            'most-common': {'strategy': most_common_strategy},
            'random': {'strategy': random_strategy},
            'naive': {'strategy': naive_strategy},
        }

        positional_counters = counters.count_positional_letters(remaining_words)
        strategy_method = methods[strategy]['strategy']
        next_guess = strategy_method(game_state, positional_counters, len(remaining_words), scorer)

    return next_guess


class NextGuessTests(unittest.TestCase):

    def test_max_info_gain(self):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        counts = counters.count_positional_letters(words)
        scorer = build_multiplier_scorer(1, 1)
        game_state = hangman.HangmanGameState('scrabbler', 'srei')
        next_guess = entropy_strategy(game_state, counts, len(words), scorer)

        self.assertEqual(next_guess, 'g')

        scorer = build_multiplier_scorer(0, 1)
        next_guess = entropy_strategy(game_state, counts, len(words), scorer)

        self.assertEqual(next_guess, 't')

        next_guess = most_common_strategy(game_state, counts, len(words), scorer)
        self.assertEqual(next_guess, 'a')

    def test_next_guess(self):
        random.seed(15243)
        choices = {
            'g': 1.75,
            't': 1.4056390622295662,
            'c': 1.4056390622295662,
            'n': 1.061278124459133,
            'u': 1.061278124459133,
            'b': 1.061278124459133,
            'l': 0.8112781244591328,
            'a': 0.8112781244591328,
            'm': 0.5435644431995964,
            'd': 0.5435644431995964,
            'o': 0.5435644431995964,
            'h': 0.5435644431995964,
            'e': 0.0,
            'r': 0.0,
            's': 0.0
        }
        game_state = hangman.HangmanGameState('scrabbler', '')
        next_guess = get_actual_next_guess(game_state, choices)
        self.assertEqual(next_guess, 'g')

    def test_tied_next_guess(self):
        random.seed(15243)
        choices = {
            't': 1.4056390622295662,
            'c': 1.4056390622295662,
            'n': 1.061278124459133,
        }
        game_state = hangman.HangmanGameState('scrabbler', '')
        next_guess = get_actual_next_guess(game_state, choices)
        self.assertEqual(next_guess, 'c')

    def test_already_guessed_next_guess(self):
        random.seed(15243)
        choices = {
            'b': 1.4056390622295662,
            'n': 1.061278124459133,
        }
        game_state = hangman.HangmanGameState('scrabbler', 'b')
        next_guess = get_actual_next_guess(game_state, choices)
        self.assertEqual(next_guess, 'n')

if __name__ == '__main__':
    from argparse import ArgumentParser
    from configparser import ConfigParser
    import csv
    import fileinput
    import os.path

    # Seed random so we can do multiple runs with same set of random words
    random.seed(15243, version=1)

    # Using argparse and ConfigParser together;
    # http://blog.vwelch.com/2011/04/combining-configparser-and-argparse.html

    parser = ArgumentParser()
    parser.add_argument('--config', metavar='CONFIG_FILE')

    args, remaining_argv = parser.parse_known_args()

    parser.add_argument('file', help='input words')
    parser.add_argument('--memory-file')
    parser.add_argument('--strategy', default='entropy-positional',
            help='Can be entropy-positional, entropy-duplicate, entropy-distinct, most-common or random')
    parser.add_argument('--scorer',
            help='multipler:2:7 - multiplier is the only available score atm')
    parser.add_argument('--entropy-scorer',
            help='multipler:2:7 - multiplier is the only available score atm')
    parser.add_argument('--reset-memory', dest='use_memory', action='store_false')
    parser.add_argument('--limit', default=1000, type=int,
            help='1000 will randomly select 1000 words to play with range')
    parser.add_argument('--range',
            help='1000:2000 will select all words within the range')

    defaults = {
        'use_memory': True
    }

    if args.config:
        config = ConfigParser()
        config.read([args.config])

        config_defaults = dict(config.items("hangman"))

        merged_defaults = dict(defaults, **config_defaults)
        parser.set_defaults(**merged_defaults)

    args = parser.parse_args(remaining_argv)

    words = [word.strip() for word in fileinput.input(args.file)]
    encoded_dictionary = dictionary.encode_dictionary(words)

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
        words_to_play = random.sample(words_to_play, args.limit)

    if args.scorer:
        scorer_type, known_multiplier, missed_multiplier = args.scorer.split(':')
        assert scorer_type == 'multiplier'
        scorer = build_multiplier_scorer(
            fractions.Fraction(known_multiplier),
            fractions.Fraction(missed_multiplier)
        )
    else:
        scorer = build_multiplier_scorer(known_multiplier=1, missed_multiplier=1)

    if args.entropy_scorer:
        entropy_scorer_type, known_multiplier, missed_multiplier = args.entropy_scorer.split(':')
        assert entropy_scorer_type == 'multiplier'
        entropy_scorer = build_multiplier_scorer(
            fractions.Fraction(known_multiplier),
            fractions.Fraction(missed_multiplier)
        )
    else:
        entropy_scorer = scorer
    scores = []
    guess_counts = []

    print(args.limit, args.strategy)
    for word in words_to_play:

        game = hangman.play(word.strip())
        for game_state in game:
            key = get_cache_key(game_state, game_state.missed_letters)
            next_guess = cached_guesses.get(key, None)
            if not next_guess:
                rejected_letters = game_state.missed_letters
                remaining_words = dictionary.filter_words(encoded_dictionary, game_state, rejected_letters)
                next_guess = get_next_guess(game_state, remaining_words, args.strategy, entropy_scorer)
                cached_guesses[key] = next_guess
            try:
                game.send(next_guess)
            except StopIteration:
                pass
        result = hangman.HangmanGameState(word, (set(game_state.guesses) | set([next_guess])))
        assert word == str(result)

        score = scorer(known_letters=len(result.known_letters), missed_letters=len(result.missed_letters))
        #print('{}: {}'.format(word, int(score)))#, result.known_letters, result.missed_letters, result.guessed_words
        scores.append(score)
        guess_counts.append(len(result.guessed_letters))

    avg = sum(scores) / float(len(scores))
    avg_guesses = sum(guess_counts) / float(len(guess_counts))

    print('Average Score: ', avg, avg_guesses)

    if args.memory_file:
        with open(args.memory_file, 'w') as memory_file:
            writer = csv.writer(memory_file)
            for key, next_guess in cached_guesses.items():
                writer.writerow([key, next_guess])
