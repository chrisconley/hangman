from collections import Counter
import unittest
from bitarray import bitarray

import dictionary

def get_key(letter, i):
    key = "{}{}".format(letter, i)
    return key

def positional_letters(word):
    for i, letter in enumerate(word):
        yield letter, i

def positional_letters(word):
    for letter in set(word):
        if letter == '-':
            continue
        yield ''.join([l if l == letter else '-' for l in word])

def encode_dictionary(words):
    encoded_dictionary = dictionary.EncodedDictionary(words)
    for word_index, word in enumerate(words):
        for key in positional_letters(word):
            bits = dictionary.set_default_bits(encoded_dictionary, key)
            bits[word_index] = True
    return encoded_dictionary

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def search(dictionary_length, encoded_dictionary, mystery_string, rejected_letters=''):
    bits = dictionary.initialize_bits(encoded_dictionary.length, True)
    for key in positional_letters(mystery_string):
        key_bits = encoded_dictionary[key]
        bits &= key_bits

    key_bits = dictionary.initialize_bits(encoded_dictionary.length, False)
    for letter in rejected_letters:
        for key in encoded_dictionary.get_keys(letter):
            letter_bits = encoded_dictionary[key]
            key_bits |= letter_bits
    key_bits.invert()
    bits &= key_bits

    return bits

class PositionalLetterTests(unittest.TestCase):

    def test_encode_dictionary(self):
        words = ['cat', 'cot', 'can']
        encoded_dictionary = encode_dictionary(words)
        expected_encoded = {
            'c--': bitarray('111'),
            '-a-': bitarray('101'),
            '-o-': bitarray('010'),
            '--n': bitarray('001'),
            '--t': bitarray('110'),
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
        self.assertEqual(search(len(words), encoded_dictionary, '-a-', rejected_letters='t'), bitarray('001'))
