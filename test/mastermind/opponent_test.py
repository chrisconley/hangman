from collections import defaultdict
import unittest

from games.mastermind import opponent, word_generator


class MastermindOpponentTests(unittest.TestCase):
    def test_get_unique_guesses_full_mastermind(self):
        words = word_generator.generate_words('ABCDEF', 4)
        self.assertEqual(opponent.get_unique_guesses(words), [
            'AAAA',
            'AAAB',
            'AABB',
            'AABC',
            'ABCD'
        ])

    def test_get_unique_guesses_short_symbols(self):
        words = word_generator.generate_words('ABC', 4)
        self.assertEqual(opponent.get_unique_guesses(words), [
            'AAAA',
            'AAAB',
            'AABB',
            'AABC',
        ])

    def test_get_unique_guesses_truncated_word_list(self):
        words = ['BBBB', 'AAAB', 'AABC']
        self.assertEqual(opponent.get_unique_guesses(words), [
            'AAAB',
            'AABC',
            'BBBB'
        ])

    def test_get_integer_partitions(self):
        # https://en.wikipedia.org/wiki/Partition_(number_theory)
        # http://stackoverflow.com/a/10036764/67184

        partitions = opponent.get_integer_partitions(4)
        self.assertEqual(partitions, {
            (4,),
            (3, 1),
            (2, 2),
            (2, 1, 1),
            (1, 1, 1, 1),
        })

        partitions = opponent.get_integer_partitions(5)
        self.assertEqual(partitions, {
            (5,),
            (4, 1),
            (3, 2),
            (3, 1, 1),
            (2, 2, 1),
            (2, 1, 1, 1),
            (1, 1, 1, 1, 1),
        })

    def test_partition_word(self):
        partition = opponent.partition_word('AAAA')
        self.assertEqual(partition, (4,))
        partition = opponent.partition_word('BBBB')
        self.assertEqual(partition, (4,))
        partition = opponent.partition_word('AABB')
        self.assertEqual(partition, (2, 2))
        partition = opponent.partition_word('AAAB')
        self.assertEqual(partition, (3, 1))
        partition = opponent.partition_word('ABBB')
        self.assertEqual(partition, (3, 1))
        partition = opponent.partition_word('ABCD')
        self.assertEqual(partition, (1, 1, 1, 1))

    def test_get_potential_next_guesses(self):
        words = ['YYY', 'YYR', 'YRY', 'RYY', 'YRR', 'RYR', 'RRY', 'RRR']
        potentials = opponent.get_potentials(words, opponent.get_response, opponent.GameLog())
        for guess, responses in potentials.items():
            print(guess, responses)
        self.assertEqual(potentials, {
            'RRR': {
                'BBB': {'RRR'}, 'BB': {'RRY', 'YRR', 'RYR'}, 'B': {'RYY', 'YYR', 'YRY'}, '': {'YYY'}
            },
            'RRY': {
                'BB': {'RRR', 'RYY', 'YRY'}, 'BWW': {'YRR', 'RYR'}, 'BBB': {'RRY'}, 'WWW': {'YYR'}, 'B': {'YYY'}
            }
        })

    def test_get_response_2211(self):
        response = opponent.get_response('2211', word_guess='1122')
        self.assertEqual(response, 'WWWW')
        words = word_generator.generate_words('123456', 4)
        responses = defaultdict(set)
        for guess in words:
            response = opponent.get_response('2211', guess)
            responses[response].add(guess)
        self.assertEqual(len(responses['WWWW']), 1)
        self.assertEqual(len(responses['WWW']), 16)

    def test_get_response_3632(self):
        response = opponent.get_response('3632', word_guess='1611')
        self.assertEqual(response, 'B')
        response = opponent.get_response('3632', word_guess='6642')
        self.assertEqual(response, 'BB')
        response = opponent.get_response('3632', word_guess='6326')
        self.assertEqual(response, 'WWW')
        response = opponent.get_response('3632', word_guess='2363')
        self.assertEqual(response, 'WWWW')
        response = opponent.get_response('3632', word_guess='6323')
        self.assertEqual(response, 'WWWW')

        response = opponent.get_response('3632', word_guess='1435')
        self.assertEqual(response, 'B')
        response = opponent.get_response('3632', word_guess='1335')
        self.assertEqual(response, 'BW')

        words = word_generator.generate_words('123456', 4)
        responses = defaultdict(set)
        for guess in words:
            response = opponent.get_response('3632', guess)
            responses[response].add(guess)
        print('----------------')
        for word in responses['WWWW']:
            print('@@@', word)
        print('length', sum([len(x) for x in responses.values()]))
        for response, words in responses.items():
            print(response, len(words))
        self.assertEqual(len(responses['WWWW']), 2)
        # self.assertEqual(len(responses['WWW']), 256)
        # self.assertEqual(len(responses['WW']), 256)
        # self.assertEqual(len(responses['W']), 256)
        # self.assertEqual(len(responses['']), 256)
        #
        # self.assertEqual(len(responses['BWWW']), 256)
        # self.assertEqual(len(responses['BWW']), 256)
        # self.assertEqual(len(responses['BW']), 256)
        # self.assertEqual(len(responses['B']), 1)

        # self.assertEqual(len(responses['BBWW']), 256)
        # self.assertEqual(len(responses['BBW']), 256)
        # self.assertEqual(len(responses['BB']), 256)
        #
        # self.assertEqual(len(responses['BBBW']), 256)
        # self.assertEqual(len(responses['BBB']), 256)
        #
        self.assertEqual(len(responses['BBBB']), 1)

        # 3632
        generated_guesses = set()
        black = '2'
        for second in ['1', '2', '4', '5']:
            for third in ['1', '2', '4', '5']:
                for fourth in ['1', '2', '4', '5']:
                    guess = ''.join([second, third, fourth, black])
                    generated_guesses.add(guess)
                    self.assertIn(guess, responses['B'])
        self.assertEqual(len(generated_guesses), 64)

        generated_guesses = set()
        black = '3'
        # --3- in 3632
        for second in ['1', '4', '5']:
            for third in ['1', '4', '5']:
                for fourth in ['1', '4', '5']:
                    guess = ''.join([second, third, black, fourth])
                    generated_guesses.add(guess)
                    self.assertIn(guess, responses['B'])
        self.assertEqual(len(generated_guesses), 256)
        self.assertEqual(len(responses['B']), 256)

        for response, words in responses.items():
            if '6662' in words:
                print('HERE IT IS', response)
