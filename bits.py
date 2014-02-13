from collections import Counter
import unittest
from bitstring import BitArray

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
                if bitarray:
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

    print 'searching'
    bitarray = search(len(words), encoded_dictionary, '---------')
    print bitarray
    print count_bitarray(bitarray)
    print get_remaining_words(bitarray, words)[0:9]
    print 'done'

    print 'searching without "h"'
    possible_letters = set(ALPHABET) - set('h')
    bitarray = search(len(words), encoded_dictionary, '---------', possible_letters=possible_letters)
    print bitarray
    print count_bitarray(bitarray)
    print 'done'

    import time
    #time.sleep(30)
