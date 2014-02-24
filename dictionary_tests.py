import unittest

import dictionary

from bitarray import bitarray

class DistinctLetterTests(unittest.TestCase):

    def test_encode_dictionary(self):
        words = ['cate', 'coth', 'cane', 'coto', 'coot']
        encoded_dictionary = dictionary.encode_dictionary(words, 'distinct')
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
        encoded_dictionary = dictionary.encode_dictionary(words, 'distinct')
        # TODO: self.AssertRaises length mismatch
        #self.assertEqual(dictionary.search(encoded_dictionary, '---'), bitarray('11111'))

        self.assertEqual(dictionary.search(encoded_dictionary, '----'), bitarray('11111'))
        self.assertEqual(dictionary.search(encoded_dictionary, '-a--'), bitarray('10100'))
        self.assertEqual(dictionary.search(encoded_dictionary, 'ca--'), bitarray('10100'))
        self.assertEqual(dictionary.search(encoded_dictionary, '-at-'), bitarray('10000'))
        self.assertEqual(dictionary.search(encoded_dictionary, 'can-'), bitarray('00100'))

        # Even though we know intuitively that '-o-o' can only match 'coto', we have only 
        # encoded our dictionary to know about distinct letters.
        self.assertEqual(dictionary.search(encoded_dictionary, '-o-o'), bitarray('01011'))

        # We don't need to dictionary.search for 'a' or 't' if we've already guessed those letters
        # Although passing it in allows us to shoot ourselves in the foot
        filtered = dictionary.search(encoded_dictionary, '-a--', rejected_letters='hot')
        self.assertEqual(filtered, bitarray('00100'))

        filtered = dictionary.search(encoded_dictionary, '-o-o', rejected_letters='aehn')
        self.assertEqual(filtered, bitarray('00011'))

        filtered = dictionary.search(encoded_dictionary, '-o-o', rejected_letters='aen')
        self.assertEqual(filtered, bitarray('01011'))

        filtered = dictionary.search(encoded_dictionary, '-o--', rejected_letters='aen')
        self.assertEqual(filtered, bitarray('01011'))

        filtered = dictionary.search(encoded_dictionary, '--t-', rejected_letters='aen')
        self.assertEqual(filtered, bitarray('01011'))

class DuplicateLetterTests(unittest.TestCase):

    def test_encode_dictionary(self):
        words = ['cate', 'coth', 'cane', 'coto', 'coot']
        encoded_dictionary = dictionary.encode_dictionary(words, 'duplicate')
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
        encoded_dictionary = dictionary.encode_dictionary(words, 'duplicate')
        # TODO: self.AssertRaises length mismatch
        #self.assertEqual(search(encoded_dictionary, '---'), bitarray('11111'))

        self.assertEqual(dictionary.search(encoded_dictionary, '----'), bitarray('11111'))
        self.assertEqual(dictionary.search(encoded_dictionary, '-a--'), bitarray('10100'))
        self.assertEqual(dictionary.search(encoded_dictionary, 'ca--'), bitarray('10100'))
        self.assertEqual(dictionary.search(encoded_dictionary, '-at-'), bitarray('10000'))
        self.assertEqual(dictionary.search(encoded_dictionary, 'can-'), bitarray('00100'))

        # Even though we know intuitively that '-o-o' can only match 'coto', we have only
        # encoded our dictionary to know about duplicate letters.
        self.assertEqual(dictionary.search(encoded_dictionary, '-o--'), bitarray('01000'))
        self.assertEqual(dictionary.search(encoded_dictionary, '-o-o'), bitarray('00011'))

        # We don't need to dictionary.search for 'a' or 't' if we've already guessed those letters
        # Although passing it in allows us to shoot ourselves in the foot
        filtered = dictionary.search(encoded_dictionary, '-a--', rejected_letters='hot')
        self.assertEqual(filtered, bitarray('00100'))

        filtered = dictionary.search(encoded_dictionary, '-o-o', rejected_letters='aehn')
        self.assertEqual(filtered, bitarray('00011'))

        filtered = dictionary.search(encoded_dictionary, '-o-o', rejected_letters='aen')
        self.assertEqual(filtered, bitarray('00011'))

        filtered = dictionary.search(encoded_dictionary, '-o--', rejected_letters='aen')
        self.assertEqual(filtered, bitarray('01000'))

        filtered = dictionary.search(encoded_dictionary, '--t-', rejected_letters='aen')
        self.assertEqual(filtered, bitarray('01011'))

class PositionalLetterTests(unittest.TestCase):

    def test_encode_dictionary(self):
        words = ['cat', 'cot', 'can']
        encoded_dictionary = dictionary.encode_dictionary(words, 'positional')
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
        encoded_dictionary = dictionary.encode_dictionary(words, 'positional')
        self.assertEqual(dictionary.search(encoded_dictionary, '---'), bitarray('111'))
        self.assertEqual(dictionary.search(encoded_dictionary, '-a-'), bitarray('101'))
        self.assertEqual(dictionary.search(encoded_dictionary, 'ca-'), bitarray('101'))
        self.assertEqual(dictionary.search(encoded_dictionary, '-at'), bitarray('100'))
        self.assertEqual(dictionary.search(encoded_dictionary, 'can'), bitarray('001'))

        # We don't need to dictionary.search for 'a' or 't' if we've already guessed those letters
        # Although passing it in allows us to shoot ourselves in the foot
        self.assertEqual(dictionary.search(encoded_dictionary, '-a-', rejected_letters='t'), bitarray('001'))
