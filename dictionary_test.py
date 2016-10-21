import unittest

import dictionary

from bitarray import bitarray


class DictionaryTests(unittest.TestCase):
    def test_encode_dictionary(self):
        words = ['cat', 'cot', 'can']
        encoded_dictionary = dictionary.encode_dictionary(words)
        expected_encoded = {
            'c0': bitarray('111'),
            'a1': bitarray('101'),
            'o1': bitarray('010'),
            'n2': bitarray('001'),
            't2': bitarray('110'),
        }
        self.assertEqual(encoded_dictionary, expected_encoded)

    def test_encode_dictionary_with_duplicates(self):
        words = ['xxoo', 'xoxo', 'xoox', 'oxxo', 'oxox', 'ooxx']
        encoded_dictionary = dictionary.encode_dictionary(words)
        expected_encoded = {
            'x0': bitarray('111000'),
            'x1': bitarray('100110'),
            'x2': bitarray('010101'),
            'x3': bitarray('001011'),
            'o0': bitarray('000111'),
            'o1': bitarray('011001'),
            'o2': bitarray('101010'),
            'o3': bitarray('110100'),
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

    def test_filter_words_with_long_words(self):
        words = ['catecatecate', 'cothcothcoth']
        encoded_dictionary = dictionary.encode_dictionary(words)

        expected_words = ['catecatecate']
        actual_words = dictionary.filter_words(encoded_dictionary, 'ca--')
        self.assertEqual(actual_words, expected_words)

    def test_filter_words_actual_first(self):
        file = open('./fixtures/nine-letter-words.txt')
        words = [line.strip() for line in file]
        file.close()
        encoded_dictionary = dictionary.encode_dictionary(words)

        actual_words = dictionary.filter_words(encoded_dictionary, '--a----le', set(['t']))
        self.assertEqual(set(actual_words), {
            'available',
            'awardable',
            'chamomile',
            'chandelle',
            'claimable',
            'coachable',
            'drapeable',
            'flammable',
            'flappable',
            'frameable',
            'frangible',
            'frankable',
            'graspable',
            'grazeable',
            'guacamole',
            'inaudible',
            'irascible',
            'leachable',
            'learnable',
            'meanwhile',
            'peaceable',
            'placeable',
            'plausible',
            'quadrille',
            'quadruple',
            'reachable',
            'scannable',
            'shakeable',
            'shapeable',
            'shareable',
            'spallable',
            'spareable',
            'unamiable',
        })

    def test_filter_words_actual_second(self):
        file = open('./fixtures/nine-letter-words.txt')
        words = [line.strip() for line in file]
        file.close()
        encoded_dictionary = dictionary.encode_dictionary(words)

        actual_words = dictionary.filter_words(encoded_dictionary, '--a--a-le', set(['t']))

        self.assertEqual(set(actual_words), {
            'available',
            'awardable',
            'claimable',
            'coachable',
            'drapeable',
            'flammable',
            'flappable',
            'frameable',
            'frankable',
            'graspable',
            'grazeable',
            'leachable',
            'learnable',
            'peaceable',
            'placeable',
            'reachable',
            'scannable',
            'shakeable',
            'shapeable',
            'shareable',
            'spallable',
            'spareable',
            'unamiable',
        })

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
        self.assertEqual(result, set(['c0', 'o1', 't2', 'o3']))

        result = set(dictionary.get_keys('-o-o'))
        self.assertEqual(result, set(['o1', 'o3']))

        result = set(dictionary.get_keys('-oto'))
        self.assertEqual(result, set(['o1', 't2', 'o3']))
