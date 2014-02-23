import unittest

import dictionary

def duplicate_letters(word):
    for letter in set(word):
        if letter == '-':
            continue
        yield ''.join([l for l in word if l == letter])

def encode_dictionary(words):
    encoded_dictionary = dictionary.EncodedDictionary(words)
    for word_index, word in enumerate(words):
        for key in duplicate_letters(word):
            bits = dictionary.set_default_bits(encoded_dictionary, key)
            bits[word_index] = True
    return encoded_dictionary

def search(encoded_dictionary, mystery_string, possible_letters=None):
    bits = dictionary.initialize_bits(encoded_dictionary.length, True)
    for key in duplicate_letters(mystery_string):
        key_bits = encoded_dictionary[key]
        bits &= key_bits

    if possible_letters:
        for key in duplicate_letters(possible_letters):
            key_bits = encoded_dictionary[key]
            bits &= key_bits

    return bits

from bitarray import bitarray
class DuplicateLetterTests(unittest.TestCase):

    def test_encode_dictionary(self):
        words = ['cate', 'coth', 'cane', 'coto', 'coot']
        encoded_dictionary = encode_dictionary(words)
        expected_encoded = {
            'c': bitarray('11111'),
            'a': bitarray('10100'),
            'o': bitarray('01000'),
            'oo': bitarray('00011'),
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
        # encoded our dictionary to know about duplicate letters.
        self.assertEqual(search(encoded_dictionary, '-o--'), bitarray('01000'))
        self.assertEqual(search(encoded_dictionary, '-o-o'), bitarray('00011'))

        # We don't need to search for 'a' or 't' if we've already guessed those letters
        # Although passing it in allows us to shoot ourselves in the foot
        filtered = search(encoded_dictionary, '-a--', possible_letters='cne')
        self.assertEqual(filtered, bitarray('00100'))

        filtered = search(encoded_dictionary, '-o-o', possible_letters='ct')
        self.assertEqual(filtered, bitarray('00011'))

        filtered = search(encoded_dictionary, '-o--', possible_letters='cth')
        self.assertEqual(filtered, bitarray('01000'))
