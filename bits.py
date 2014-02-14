from collections import Counter
import unittest
from bitarray import bitarray
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
            barray  = encoded_dictionary.get(key, None)
            if barray is None:
                barray = bitarray(dictionary_length)
                barray[0:] = False
                encoded_dictionary[key] = barray
            barray[word_index] = True
    return encoded_dictionary

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def search(dictionary_length, graph, mystery_string, possible_letters=ALPHABET):
    union = bitarray(dictionary_length)
    union[0:] = True
    word_length = len(mystery_string)
    for i, mystery_letter in enumerate(mystery_string):
        if mystery_letter == '-':
            array = bitarray(dictionary_length)
            array[0:] = False
            for letter in possible_letters:
                key = get_key(letter, i)
                barray = graph.get(key, None)
                if barray is not None:
                    array |= barray
            barray = array
        else:
            key = get_key(mystery_letter, i)
            barray = graph[key]
        union &= barray

    return union

def count_bitarray(barray):
    count = len([x for x in barray if x])
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
            'c0': bitarray('111'),
            'a1': bitarray('101'),
            'o1': bitarray('010'),
            'n2': bitarray('001'),
            't2': bitarray('110'),
        }
        self.assertEqual(encoded_dictionary, expected_encoded)

    def test_search(self):
        words = ['cat', 'cot', 'can']
        encoded_dictionary = encode_dictionary(words)
        self.assertEqual(search(len(words), encoded_dictionary, '---'), bitarray('111'))
        self.assertEqual(search(len(words), encoded_dictionary, '-a-'), bitarray('101'))
        self.assertEqual(search(len(words), encoded_dictionary, 'ca-'), bitarray('101'))
        self.assertEqual(search(len(words), encoded_dictionary, '-at'), bitarray('100'))
        self.assertEqual(search(len(words), encoded_dictionary, 'can'), bitarray('001'))

        # We don't need to search for 'a' or 't' if we've already guessed those letters
        # Although passing it in allows us to shoot ourselves in the foot
        self.assertEqual(search(len(words), encoded_dictionary, '-a-', possible_letters='cn'), bitarray('001'))

    def test_count_bitarray(self):
        self.assertEqual(count_bitarray(bitarray('111')), 3)
        self.assertEqual(count_bitarray(bitarray('110')), 2)
        self.assertEqual(count_bitarray(bitarray('001')), 1)

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

    print 'playing'
    cached_guesses = {}
    scores = []
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
                counts = count_positional_letters(remaining_words)
                guesses = strategy(mystery_string, counts)
                cached_guesses[key] = guesses
            try:
                g.send(guesses)
            except StopIteration:
                result = mystery_string

        scores.append(game.default_scorer(result))

    avg = sum(scores) / float(len(scores))
    print 'Average Score: ', avg
