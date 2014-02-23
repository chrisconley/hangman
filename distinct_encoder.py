import unittest

import dictionary

def distinct_letters(word):
    for letter in set(word):
        if letter == '-':
            continue
        yield letter

def encode_dictionary(words):
    encoded_dictionary = dictionary.EncodedDictionary(words)
    for word_index, word in enumerate(words):
        for key in distinct_letters(word):
            bits = dictionary.set_default_bits(encoded_dictionary, key)
            bits[word_index] = True
    return encoded_dictionary

def search(encoded_dictionary, mystery_string):
    union = dictionary.initialize_bits(encoded_dictionary.length, True)
    for key in distinct_letters(mystery_string):
        barray = encoded_dictionary[key]
        union &= barray

    return union

from bitarray import bitarray
class DistinctLetterTests(unittest.TestCase):

    def test_encode_dictionary(self):
        words = ['cate', 'coth', 'cane', 'coto', 'coot']
        encoded_dictionary = encode_dictionary(words)
        expected_encoded = {
            'c': bitarray('11111'),
            'a': bitarray('10100'),
            'o': bitarray('01011'),
            'n': bitarray('00100'),
            't': bitarray('11011'),
            'e': bitarray('10100'),
            'h': bitarray('01000'),
        }
        self.assertEqual(encoded_dictionary, expected_encoded)

    def test_search(self):
        words = ['cate', 'coth', 'cane', 'coto', 'coot']
        encoded_dictionary = encode_dictionary(words)
        # TODO: self.AssertRaises length mismatch
        #self.assertEqual(search(encoded_dictionary, '---'), bitarray('11111'))

        self.assertEqual(search(encoded_dictionary, '----'), bitarray('11111'))
        self.assertEqual(search(encoded_dictionary, '-a--'), bitarray('10100'))
        self.assertEqual(search(encoded_dictionary, 'ca--'), bitarray('10100'))
        self.assertEqual(search(encoded_dictionary, '-at-'), bitarray('10000'))
        self.assertEqual(search(encoded_dictionary, 'can-'), bitarray('00100'))

        # Even though we know intuitively that '-o-o' can only match 'coto', we have only 
        # encoded our dictionary to know about distinct letters.
        self.assertEqual(search(encoded_dictionary, '-o-o'), bitarray('01011'))
