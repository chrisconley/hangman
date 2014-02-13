from collections import Counter
import unittest
from bitstring import BitArray

from hangman import game

def get_key(letter, i):
    key = "{}{}".format(letter, i)
    return key

def encode_dictionary(words):
    encoded_dictionary = {}
    dictionary_length = len(words)
    for word_index, word in enumerate(words):
        word_length = len(word)
        for i, letter in enumerate(word):
            key = get_key(letter, i)
            bitarray = encoded_dictionary.setdefault(key, BitArray(dictionary_length))
            bitarray.set(1, word_index)
    return encoded_dictionary

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def search(dictionary_length, graph, mystery_string, possible_letters=ALPHABET):
    union = BitArray(dictionary_length)
    union.invert()
    word_length = len(mystery_string)
    for i, mystery_letter in enumerate(mystery_string):
        if mystery_letter == '-':
            array = BitArray(dictionary_length)
            for letter in possible_letters:
                key = get_key(letter, i)
                bitarray = graph.get(key, None)
                if bitarray is not None:
                    array |= bitarray
            bitarray = array
        else:
            key = get_key(mystery_letter, i)
            bitarray = graph[key]
        union &= bitarray

    return union

def count_bitarray(bitarray):
    count = len([x for x in bitarray if x])
    return count

def get_remaining_words(encoded_words, words):
    return [words[index] for (index, bit) in enumerate(encoded_words) if bit]

def count_distinct_letters(words):
    counter = Counter()
    for word in words:
        for letter in set(word):
            counter[letter] += 1
    return counter

def count_duplicate_letters(words):
    counts = {}
    for word in words:
        for letter in set(word):
            counter = counts.setdefault(letter, Counter())
            key = "".join([l for l in word if l == letter])
            #print word, letter, key
            counter[key] += 1
            counter['*'] += 1
    return counts

def count_positional_letters(words):
    counts = {}
    for word in words:
        for letter in set(word):
            counter = counts.setdefault(letter, Counter())
            key = "".join([l if l == letter else '-' for l in word])
            #print word, letter, key
            counter[key] += 1
            counter['*'] += 1
    return counts

class BitCounter(unittest.TestCase):

    def test_encode_dictionary(self):
        words = ['cat', 'cot', 'can']
        encoded_dictionary = encode_dictionary(words)
        expected_encoded = {
            'c0': BitArray('0b111'),
            'a1': BitArray('0b101'),
            'o1': BitArray('0b010'),
            'n2': BitArray('0b001'),
            't2': BitArray('0b110'),
        }
        self.assertEqual(encoded_dictionary, expected_encoded)

    def test_search(self):
        words = ['cat', 'cot', 'can']
        encoded_dictionary = encode_dictionary(words)
        self.assertEqual(search(len(words), encoded_dictionary, '---'), BitArray('0b111'))
        self.assertEqual(search(len(words), encoded_dictionary, '-a-'), BitArray('0b101'))
        self.assertEqual(search(len(words), encoded_dictionary, 'ca-'), BitArray('0b101'))
        self.assertEqual(search(len(words), encoded_dictionary, '-at'), BitArray('0b100'))
        self.assertEqual(search(len(words), encoded_dictionary, 'can'), BitArray('0b001'))

        # We don't need to search for 'a' or 't' if we've already guessed those letters
        # Although passing it in allows us to shoot ourselves in the foot
        self.assertEqual(search(len(words), encoded_dictionary, '-a-', possible_letters='cn'), BitArray('0b001'))

    def test_count_bitarray(self):
        self.assertEqual(count_bitarray(BitArray('0b111')), 3)
        self.assertEqual(count_bitarray(BitArray('0b110')), 2)
        self.assertEqual(count_bitarray(BitArray('0b001')), 1)

    def test_get_remaining_words(self):
        words = ['cat', 'cot', 'can']
        encoded_dictionary = encode_dictionary(words)

        encoded_words = search(len(words), encoded_dictionary, '-a-', possible_letters='cn')
        remaining_words = get_remaining_words(encoded_words, words)
        self.assertEqual(remaining_words, ['can'])

        encoded_words = search(len(words), encoded_dictionary, 'ca-', possible_letters='cnt')
        remaining_words = get_remaining_words(encoded_words, words)
        self.assertEqual(remaining_words, ['cat', 'can'])

    def test_count_distinct_letters(self):
        words = ['cat', 'cot', 'can', 'coto']
        counter = count_distinct_letters(words)
        self.assertEqual(counter['a'], 2)
        self.assertEqual(counter['c'], 4)
        self.assertEqual(counter['n'], 1)
        self.assertEqual(counter['o'], 2)
        self.assertEqual(counter['t'], 3)

    def test_count_duplicate_letters(self):
        words = ['cat', 'cot', 'can', 'coto']
        counter = count_duplicate_letters(words)
        self.assertEqual(counter['a'], {'*': 2, 'a': 2})
        self.assertEqual(counter['c'], {'*': 4, 'c': 4})
        self.assertEqual(counter['n'], {'*': 1, 'n': 1})
        self.assertEqual(counter['o'], {'*': 2, 'o': 1, 'oo': 1})
        self.assertEqual(counter['t'], {'*': 3, 't': 3})

    def test_count_positional_letters(self):
        words = ['cat', 'cot', 'can', 'coto', 'coot']
        counter = count_positional_letters(words)
        self.assertEqual(counter['a'], {'*': 2, '-a-': 2})
        self.assertEqual(counter['c'], {'*': 5, 'c--': 3, 'c---': 2})
        self.assertEqual(counter['n'], {'*': 1, '--n': 1})
        self.assertEqual(counter['o'], {'*': 3, '-o-': 1, '-o-o': 1, '-oo-': 1})
        self.assertEqual(counter['t'], {'*': 4, '--t': 2, '--t-': 1, '---t': 1})

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

    #print 'searching'
    #bitarray = search(len(words), encoded_dictionary, '---------')
    #print bitarray
    #print count_bitarray(bitarray)
    #remaining_words = get_remaining_words(bitarray, words)
    #counts = count_positional_letters(remaining_words)
    ## TODO: Just need to hook up to hangman.game now
    #print 'done'

    #print 'searching without "h"'
    #possible_letters = set(ALPHABET) - set('h')
    #bitarray = search(len(words), encoded_dictionary, '---------', possible_letters=possible_letters)
    #print bitarray
    #print count_bitarray(bitarray)
    #print 'done'

    print 'playing'
    cached_guesses = {}
    for word in words[8000:8010]:
        print word
        g = game.play(word.strip(), strategy=strategy)
        result = ''
        for mystery_string in g:
            key = "{}:{}".format(mystery_string, sorted("".join(mystery_string.missed_letters)))
            guesses = cached_guesses.get(key, None)
            if not guesses:
                possible_letters = set(ALPHABET) - set(mystery_string.guesses)
                encoded_remaining_words = search(len(words), encoded_dictionary, mystery_string, possible_letters=possible_letters)
                remaining_words = get_remaining_words(encoded_remaining_words, words)
                counts = count_positional_letters(remaining_words)
                guesses = strategy(mystery_string, counts)
                cached_guesses[key] = guesses
            try:
                g.send(guesses)
            except StopIteration:
                result = mystery_string

        print result, result.known_letters, result.missed_letters
        print 'score: ', game.default_scorer(result)

