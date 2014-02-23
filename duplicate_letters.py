from bitarray import bitarray
import unittest

class EncodedDictionary(dict):
    def __init__(self, words, *args, **kwargs):
        self.words = words
        self.length = len(words)
        super(dict, self).__init__()

def initialize_bits(length, initializer=False):
    array = bitarray(length)
    array[0:] = initializer
    return array

def set_default_bits(encoded_dictionary, key):
    bits = encoded_dictionary.get(key)
    if bits is None:
        bits = initialize_bits(encoded_dictionary.length)
        encoded_dictionary[key] = bits
    return encoded_dictionary[key]

def duplicate_letters(word):
    for letter in set(word):
        if letter == '-':
            continue
        yield ''.join([l for l in word if l == letter])

def encode_dictionary(words):
    encoded_dictionary = EncodedDictionary(words)
    for word_index, word in enumerate(words):
        word_length = len(word)
        for key in duplicate_letters(word):
            bits = set_default_bits(encoded_dictionary, key)
            bits[word_index] = True
    return encoded_dictionary

def search(encoded_dictionary, mystery_string):
    union = initialize_bits(encoded_dictionary.length, True)
    word_length = len(mystery_string)
    for key in duplicate_letters(mystery_string):
        barray = encoded_dictionary[key]
        union &= barray

    return union

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

