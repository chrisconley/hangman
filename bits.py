from collections import Counter
import unittest
from bitarray import bitarray
from hangman import game
import entropy


# Baseline
random

# Initial Knowledge
naive

# Knowledge at each step
distinct, duplicate, positional
use missed letters or not

# Knowledge you'll gain / strategy
most common, distinct letter entropy, duplicate letter entropy, positional letter entropy

def get_remaining_words(encoded_words, words):
    return [words[index] for (index, bit) in enumerate(encoded_words) if bit]

class BitCounter(unittest.TestCase):

    def test_get_remaining_words(self):
        words = ['cat', 'cot', 'can']
        encoded_words = bitarray('001')
        remaining_words = get_remaining_words(encoded_words, words)
        self.assertEqual(remaining_words, ['can'])

        encoded_words = bitarray('101')
        remaining_words = get_remaining_words(encoded_words, words)
        self.assertEqual(remaining_words, ['cat', 'can'])

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
            return mystery_string.guesses | set(letter)

def other_scorer(result):
    if len(result.missed_words) >= 5:
        return 25
    else:
        return (len(result.guesses) * 1) + (len(result.missed_words) * 1)

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import fileinput

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    args = parser.parse_args()

    words = [word.strip() for word in fileinput.input(args.file)]
    print len(words)
    encoded_dictionary = encode_dictionary(words)

    #for key, a in encoded_dictionary.items():
        #print key, a
    print len(encoded_dictionary.keys())

    print 'playing'
    cached_guesses = {}
    scores = []
    other_scores = []
    for word in words:
        g = game.play(word.strip(), strategy=strategy)
        result = ''
        for mystery_string in g:
            key = "{}:{}".format(mystery_string, sorted("".join(mystery_string.missed_letters)))
            guesses = cached_guesses.get(key, None)
            if not guesses:
                possible_letters = set(ALPHABET) - set(mystery_string.guesses)
                encoded_remaining_words = search(len(words), encoded_dictionary, mystery_string, possible_letters=possible_letters)
                remaining_words = get_remaining_words(encoded_remaining_words, words)
                counts = count_duplicate_letters(remaining_words)
                guesses = entropy_strategy(mystery_string, counts, len(remaining_words))
                cached_guesses[key] = guesses
            try:
                g.send(guesses)
            except StopIteration:
                result = mystery_string

        scores.append(game.default_scorer(result))
        other_scores.append(other_scorer(result))

    avg = sum(scores) / float(len(scores))
    other_avg = sum(other_scores) / float(len(other_scores))
    print 'Average Score: ', avg
    print 'Average Other Score: ', other_avg
