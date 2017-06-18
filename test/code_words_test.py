import unittest

from bitarray import bitarray

from games import code_words


class CodeWordsTests(unittest.TestCase):
    def test_get_partial_dictionary(self):
        dictionary = code_words.Dictionary(['cat', 'bat'])
        result = dictionary.get_partial_dictionary({'bat'})
        self.assertEqual(result.as_bits, bitarray('01'))
        self.assertEqual(result.as_words, {'bat'})
        self.assertEqual(result.all_words, ['cat', 'bat'])

    def test_words_to_bits(self):
        dictionary = code_words.Dictionary(['cat', 'bat'])
        result = dictionary.words_to_bits({'bat'})
        self.assertEqual(result, bitarray('01'))

        result = dictionary.words_to_bits({'cat'})
        self.assertEqual(result, bitarray('10'))

        result = dictionary.words_to_bits({'bat', 'cat'})
        self.assertEqual(result, bitarray('11'))

    def test_bits_to_words(self):
        dictionary = code_words.Dictionary(['cat', 'bat'])
        result = dictionary.bits_to_words(bitarray('01'))
        self.assertEqual(result, {'bat'})

        result = dictionary.bits_to_words(bitarray('10'))
        self.assertEqual(result, {'cat'})

        result = dictionary.bits_to_words(bitarray('11'))
        self.assertEqual(result, {'cat', 'bat'})
