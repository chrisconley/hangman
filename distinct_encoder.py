from bitarray import bitarray
import unittest

def get_key(letter):
    return letter

def encode_dictionary(words):
    encoded_dictionary = {}
    dictionary_length = len(words)
    for word_index, word in enumerate(words):
        word_length = len(word)
        for i, letter in enumerate(set(word)):
            key = get_key(letter)
            barray  = encoded_dictionary.get(key, None)
            if barray is None:
                barray = bitarray(dictionary_length)
                barray[0:] = False
                encoded_dictionary[key] = barray
            barray[word_index] = True
    return encoded_dictionary

def search(dictionary_length, graph, mystery_string):
    union = bitarray(dictionary_length)
    union[0:] = True # initialize all bits to 1
    word_length = len(mystery_string)
    for i, mystery_letter in enumerate(set(mystery_string)):
        if mystery_letter != '-':
            key = get_key(mystery_letter)
            barray = graph[key]
            union &= barray

    return union

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
        #self.assertEqual(search(len(words), encoded_dictionary, '---'), bitarray('11111'))

        self.assertEqual(search(len(words), encoded_dictionary, '----'), bitarray('11111'))
        self.assertEqual(search(len(words), encoded_dictionary, '-a--'), bitarray('10100'))
        self.assertEqual(search(len(words), encoded_dictionary, 'ca--'), bitarray('10100'))
        self.assertEqual(search(len(words), encoded_dictionary, '-at-'), bitarray('10000'))
        self.assertEqual(search(len(words), encoded_dictionary, 'can-'), bitarray('00100'))

        # Even though we know intuitively that '-o-o' can only match 'coto', we have only 
        # encoded our dictionary to know about distinct letters.
        self.assertEqual(search(len(words), encoded_dictionary, '-o-o'), bitarray('01011'))
