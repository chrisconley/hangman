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

def encode_dictionary(words):
    encoded_dictionary = dictionary.EncodedDictionary(words)
    for word_index, word in enumerate(words):
        for letter, position in positional_letters(word):
            key = get_key(letter, position)
            bits = dictionary.set_default_bits(encoded_dictionary, key)
            bits[word_index] = True
    return encoded_dictionary

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def search(dictionary_length, encoded_dictionary, mystery_string, possible_letters=None):
    bits = dictionary.initialize_bits(encoded_dictionary.length, True)
    for mystery_letter, position in positional_letters(mystery_string):
        key = get_key(mystery_letter, position)
        if mystery_letter == '-' and possible_letters:
            key_bits = dictionary.initialize_bits(encoded_dictionary.length, False)
            for letter in possible_letters:
                key = get_key(letter, position)
                letter_bits = encoded_dictionary.get(key, None)
                if letter_bits is not None:
                    key_bits |= letter_bits
            bits &= key_bits
        elif mystery_letter != '-':
            key_bits = encoded_dictionary[key]
            bits &= key_bits

    return bits

class PositionalLetterTests(unittest.TestCase):

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
