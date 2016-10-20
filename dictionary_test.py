import unittest

import dictionary

from bitarray import bitarray


class DictionaryTests(unittest.TestCase):
    def test_encode_dictionary(self):
        words = ['cat', 'cot', 'can']
        encoded_dictionary = dictionary.encode_dictionary(words)
        expected_encoded = {
            'c--': bitarray('111'),
            '-a-': bitarray('101'),
            '-o-': bitarray('010'),
            '--n': bitarray('001'),
            '--t': bitarray('110'),
        }
        self.assertEqual(encoded_dictionary, expected_encoded)

    def test_filter_words(self):
        words = ['cate', 'coth', 'cane', 'coto', 'coot']
        encoded_dictionary = dictionary.encode_dictionary(words)

        expected_words = ['cate', 'cane']
        actual_words = dictionary.filter_words(encoded_dictionary, 'ca--')
        self.assertEqual(actual_words, expected_words)

        expected_words = ['cate']
        actual_words = dictionary.filter_words(encoded_dictionary, 'ca--', 'n')
        self.assertEqual(actual_words, expected_words)

    def test_search(self):
        words = ['cat', 'cot', 'can']
        encoded_dictionary = dictionary.encode_dictionary(words)
        self.assertEqual(dictionary.search(encoded_dictionary, '---'), bitarray('111'))
        self.assertEqual(dictionary.search(encoded_dictionary, '-a-'), bitarray('101'))
        self.assertEqual(dictionary.search(encoded_dictionary, 'ca-'), bitarray('101'))
        self.assertEqual(dictionary.search(encoded_dictionary, '-at'), bitarray('100'))
        self.assertEqual(dictionary.search(encoded_dictionary, 'can'), bitarray('001'))

        # We don't need to dictionary.search for 'a' or 't' if we've already guessed those letters
        # Although passing it in allows us to shoot ourselves in the foot
        self.assertEqual(dictionary.search(encoded_dictionary, '-a-', rejected_letters='t'), bitarray('001'))

    def test_get_remaining_words(self):
        words = ['cat', 'cot', 'can']
        encoded_words = bitarray('001')
        remaining_words = dictionary.get_remaining_words(encoded_words, words)
        self.assertEqual(remaining_words, ['can'])

        encoded_words = bitarray('101')
        remaining_words = dictionary.get_remaining_words(encoded_words, words)
        self.assertEqual(remaining_words, ['cat', 'can'])

    def test_get_keys(self):
        result = set(dictionary.get_keys('coto'))
        self.assertEqual(result, set(['c---', '--t-', '-o-o']))

        result = set(dictionary.get_keys('-o-o'))
        self.assertEqual(result, set(['-o-o']))

        result = set(dictionary.get_keys('-oto'))
        self.assertEqual(result, set(['--t-', '-o-o']))
