from collections import Counter
import unittest
from bitarray import bitarray

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
    union[0:] = True # initialize all bits to 1
    word_length = len(mystery_string)
    for i, mystery_letter in enumerate(mystery_string):
        if mystery_letter == '-':
            array = bitarray(dictionary_length)
            array[0:] = False # initalize all bits to 0
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
