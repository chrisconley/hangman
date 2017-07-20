import random
import unittest

import games.code_words
from games.hangman import opponent


class HangmanOpponentTests(unittest.TestCase):
    def test_get_response(self):
        result = opponent.get_response('cat', 't')
        self.assertEqual(result, '--t')

        result = opponent.get_response('cat', 's')
        self.assertEqual(result, '!')

        result = opponent.get_response('cat', 'cat')
        self.assertEqual(result, 'cat')

        result = opponent.get_response('cat', 'can')
        self.assertEqual(result, '!')

    def test_get_cache_key(self):
        game_log = opponent.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r-----r'},
            {'guess': 'e', 'result': '------e--'},
            {'guess': 'i', 'result': '!'},
            {'guess': 'a', 'result': '!'},
        ])

        cache_key = game_log.get_cache_key()
        self.assertEqual(cache_key, 's-r---e-r:ai')

    def test_get_cache_key_when_no_correct_guesses(self):
        game_log = opponent.GameLog([
            {'guess': 'i', 'result': '!'},
            {'guess': 'a', 'result': '!'},
        ])

        cache_key = game_log.get_cache_key()
        self.assertEqual(cache_key, ':ai')

    def test_get_cache_key_when_no_missed_guesses(self):
        game_log = opponent.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r-----r'},
            {'guess': 'e', 'result': '------e--'},
        ])

        cache_key = game_log.get_cache_key()
        self.assertEqual(cache_key, 's-r---e-r:')


class HangmanPotentialsTests(unittest.TestCase):
    def test_get_potentials(self):
        words = ['cat', 'bat']
        words = games.code_words.Dictionary(words).get_partial_dictionary(set(words))
        potentials = opponent.get_potentials(words, opponent.get_response, opponent.GameLog())
        self.assertEqual(potentials, {
            'a': {
                '-a-': {'cat', 'bat'}
            },
            'b': {
                'b--': {'bat'}, '!': {'cat'}
            },
            'c': {
                'c--': {'cat'}, '!': {'bat'}
            },
            't': {
                '--t': {'cat', 'bat'}
            }
        })
