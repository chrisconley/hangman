from collections import defaultdict
import unittest

from games.mastermind import opponent, word_generator
from games import code_words


class MastermindOpponentTests(unittest.TestCase):
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
        self.assertEqual(response, 'WWWW')
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

        self.assertEqual(sum([len(x) for x in responses.values()]), 1296)
        self.assertEqual(len(responses['WWWW']), 16)
        self.assertEqual(len(responses['WWW']), 96)
        self.assertEqual(len(responses['WW']), 216)
        self.assertEqual(len(responses['W']), 216)
        self.assertEqual(len(responses['']), 81)

        self.assertEqual(len(responses['BWWW']), 18)
        self.assertEqual(len(responses['BWW']), 96)
        self.assertEqual(len(responses['BW']), 204)
        self.assertEqual(len(responses['B']), 182)

        self.assertEqual(len(responses['BBWW']), 5)
        self.assertEqual(len(responses['BBW']), 40)
        self.assertEqual(len(responses['BB']), 105)

        self.assertEqual(len(responses['BBBW']), 0)
        self.assertEqual(len(responses['BBB']), 20)
        self.assertEqual(len(responses['BBBB']), 1)

    def test_get_response_2211_alternative(self):
        response = opponent.get_response_alternative('2211', word_guess='1122')
        self.assertEqual(response, 'WWWW')
        words = word_generator.generate_words('123456', 4)
        responses = defaultdict(set)
        for guess in words:
            response = opponent.get_response_alternative('2211', guess)
            responses[response].add(guess)
        self.assertEqual(len(responses['WWWW']), 1)
        self.assertEqual(len(responses['WWW']), 16)

    def test_get_response_3632_alternative(self):
        response = opponent.get_response_alternative('3632', word_guess='1611')
        self.assertEqual(response, 'B')
        response = opponent.get_response_alternative('3632', word_guess='6642')
        self.assertEqual(response, 'BB')
        response = opponent.get_response_alternative('3632', word_guess='6326')
        self.assertEqual(response, 'WWW')
        response = opponent.get_response_alternative('3632', word_guess='2363')
        self.assertEqual(response, 'WWWW')
        response = opponent.get_response_alternative('3632', word_guess='6323')
        self.assertEqual(response, 'WWWW')

        response = opponent.get_response_alternative('3632', word_guess='1435')
        self.assertEqual(response, 'B')
        response = opponent.get_response_alternative('3632', word_guess='1335')
        self.assertEqual(response, 'BW')

        words = word_generator.generate_words('123456', 4)
        responses = defaultdict(set)
        for guess in words:
            response = opponent.get_response_alternative('3632', guess)
            responses[response].add(guess)

        self.assertEqual(sum([len(x) for x in responses.values()]), 1296)
        self.assertEqual(len(responses['WWWW']), 2)
        self.assertEqual(len(responses['WWW']), 44)
        self.assertEqual(len(responses['WW']), 222)
        self.assertEqual(len(responses['W']), 276)
        self.assertEqual(len(responses['']), 81)

        self.assertEqual(len(responses['BWWW']), 4)
        self.assertEqual(len(responses['BWW']), 84)
        self.assertEqual(len(responses['BW']), 230)
        self.assertEqual(len(responses['B']), 182)

        self.assertEqual(len(responses['BBWW']), 5)
        self.assertEqual(len(responses['BBW']), 40)
        self.assertEqual(len(responses['BB']), 105)

        self.assertEqual(len(responses['BBBW']), 0)
        self.assertEqual(len(responses['BBB']), 20)
        self.assertEqual(len(responses['BBBB']), 1)

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

    def test_get_potential_next_guesses_alternative(self):
        all_words = ['YYY', 'YYR', 'YRY', 'RYY', 'YRR', 'RYR', 'RRY', 'RRR']
        dictionary = code_words.Dictionary(all_words)
        words = dictionary.get_partial_dictionary(set(all_words))
        potentials = opponent.get_potentials(words, opponent.get_response_alternative, opponent.GameLog())

        self.assertEqual(potentials['RRR'], {
            'BBB': {'RRR'}, 'BB': {'RRY', 'YRR', 'RYR'}, 'B': {'RYY', 'YYR', 'YRY'}, '': {'YYY'}
        })
        self.assertEqual(potentials['RRY'], {
            'BB': {'RRR', 'RYY', 'YRY'}, 'BWW': {'YRR', 'RYR'}, 'BBB': {'RRY'}, 'B': {'YYY'}, 'WW': {'YYR'}
        })


class MastermindGameLogTests(unittest.TestCase):
    def test_cache_key_sorts_properly(self):
        game_log = opponent.GameLog([
            {'guess': '123', 'result': 'BB'},
            {'guess': '321', 'result': 'BBW'},
        ])
        self.assertEqual(game_log.get_cache_key(), '123BB:321BBW')

        game_log = opponent.GameLog([
            {'guess': '321', 'result': 'BBW'},
            {'guess': '123', 'result': 'BB'},
        ])
        self.assertEqual(game_log.get_cache_key(), '321BBW:123BB')

    def test_cache_key_empty_game_log(self):
        game_log = opponent.GameLog()
        self.assertEqual(game_log.get_cache_key(), 'START')
