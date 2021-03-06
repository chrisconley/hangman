from decimal import Decimal
import random
import unittest

from games import player_utils
from games.hangman import opponent, player
import games.code_words


class HangmanPlayerTests(unittest.TestCase):
    def assertDecimalAlmostEqual(self, actual, expected, places):
        self.assertEqual(type(actual), Decimal)
        self.assertAlmostEqual(float(actual), float(expected), places=places)

    def test_build_weighted_product_strategy(self):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        words = games.code_words.Dictionary(words).get_partial_dictionary(set(words))
        game_log = opponent.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r-----r'},
            {'guess': 'e', 'result': '-------e-'},
            {'guess': 'i', 'result': '!'},
        ])
        potentials = opponent.get_potentials(words, opponent.get_response, game_log)

        strategy = player.build_strategy({'info': 1.0}, model=player_utils.weighted_product)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'g')

        info = 0.505
        reward = 1.0 - info
        strategy = player.build_strategy({'info': info, 'reward': reward}, model=player_utils.weighted_product)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'g')

        info = 0.504
        reward = 1.0 - info
        strategy = player.build_strategy({'info': info, 'reward': reward}, model=player_utils.weighted_product)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 't')

        strategy = player.build_strategy({'reward': 1.0}, model=player_utils.weighted_product)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'a')

    def test_build_weighted_sum_strategy(self):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        words = games.code_words.Dictionary(words).get_partial_dictionary(set(words))
        game_log = opponent.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r-----r'},
            {'guess': 'e', 'result': '-------e-'},
            {'guess': 'i', 'result': '!'},
        ])
        potentials = opponent.get_potentials(words, opponent.get_response, game_log)

        strategy = player.build_strategy({'info': 1.0}, model=player_utils.weighted_sum)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'g')

        strategy = player.build_strategy({'info': 0.37, 'reward': 0.63}, model=player_utils.weighted_sum)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'g')

        strategy = player.build_strategy({'info': 0.36, 'reward': 0.64}, model=player_utils.weighted_sum)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 't')

        strategy = player.build_strategy({'reward': 1.0}, model=player_utils.weighted_sum)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'a')

    def test_build_strategy_final_word_guess(self):
        random.seed(15243)
        words = ['scrabbler']
        words = games.code_words.Dictionary(words).get_partial_dictionary(set(words))
        game_log = opponent.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r-----r'},
            {'guess': 'e', 'result': '-------e-'},
            {'guess': 'i', 'result': '!'},
        ])
        potentials = opponent.get_potentials(words, opponent.get_response, game_log)

        strategy = player.build_strategy({}, model=player_utils.weighted_sum)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'scrabbler')

    def test_get_next_guess_naive(self):
        potentials = games.code_words.PotentialOutcomes({
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
        next_guess = player.get_next_guess_naive(potentials, opponent.GameLog())
        self.assertEqual(next_guess, 'a')

    def test_get_next_guess_naive_with_game_log(self):
        potentials = games.code_words.PotentialOutcomes({
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
        game_log = opponent.GameLog([{'guess': 'a', 'result': '-a-'}])
        next_guess = player.get_next_guess_naive(potentials, game_log)
        self.assertEqual(next_guess, 't')

    def test_get_next_guess_naive_with_one_word_left(self):
        potentials = games.code_words.PotentialOutcomes({
            'b': {
                'b--': {'bat'}
            },
            'c': {
                '!': {'bat'}
            },
            't': {
                '--t': {'bat'}
            }
        })
        game_log = opponent.GameLog([{'guess': 'a', 'result': '-a-'}])
        next_guess = player.get_next_guess_naive(potentials, game_log)
        self.assertEqual(next_guess, 'bat')

    def test_get_pmf_for_success(self):
        possible_responses = games.code_words.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar'}
        })
        pmf = player._get_pmf_for_success(possible_responses)
        self.assertDecimalAlmostEqual(pmf['*'], Decimal('0.40000000000000'), places=17)
        self.assertDecimalAlmostEqual(pmf['!'], Decimal('0.60000000000000'), places=17)

        possible_responses = games.code_words.PossibleResponses.from_dict('d', {
            '!': {'bar', 'tab', 'tar', 'ace', 'cat'}
        })
        pmf = player._get_pmf_for_success(possible_responses)
        self.assertDecimalAlmostEqual(pmf['*'], Decimal('0.00000000000000'), places=17)
        self.assertDecimalAlmostEqual(pmf['!'], Decimal('1.00000000000000'), places=17)

    def test_get_pmf_for_success_raises_if_duplicate_invalid_codewords(self):
        possible_responses = games.code_words.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace', 'cat'},
            '!': {'bar', 'tab', 'tar'}
        })
        with self.assertRaises(AssertionError):
            player._get_pmf_for_success(possible_responses)

        possible_responses = games.code_words.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar', 'cat'}
        })
        with self.assertRaises(AssertionError):
            player._get_pmf_for_success(possible_responses)

    #
    # @patch('games.hangman.player.get_actual_next_guess', return_value='hi')
    # def test_build_strategy_does_not_cache_counts_by_default(self, get_next_guess):
    #     random.seed(15243)
    #     words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
    #              'straddler', 'straggler', 'strangler', 'struggler'
    #              ]
    #     words = games.code_words.Dictionary(words).get_partial_dictionary(set(words))
    #     game_log = opponent.GameLog([
    #         {'guess': 's', 'result': 's--------'},
    #         {'guess': 'r', 'result': '--r-----r'},
    #         {'guess': 'e', 'result': '-------e-'},
    #         {'guess': 'i', 'result': '!'},
    #     ])
    #     potentials = opponent.get_potentials(words, opponent.get_response, game_log)
    #
    #     strategy = player.build_strategy(info_focus=1.0, success_focus=0.0, final_word_guess=True)
    #     next_guess = strategy(potentials, game_log)
    #     next_guess = strategy(potentials, game_log)
    #     self.assertEqual(next_guess, 'hi')
    #
    #     self.assertEqual(get_next_guess.call_count, 2)
    #
    # @patch('games.hangman.player.get_actual_next_guess', return_value='hi')
    # def test_build_strategy_does_cache_counts_when_use_cache_is_true(self, get_next_guess):
    #     random.seed(15243)
    #     words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
    #              'straddler', 'straggler', 'strangler', 'struggler'
    #              ]
    #     words = games.code_words.Dictionary(words).get_partial_dictionary(set(words))
    #     game_log = opponent.GameLog([
    #         {'guess': 's', 'result': 's--------'},
    #         {'guess': 'r', 'result': '--r-----r'},
    #         {'guess': 'e', 'result': '-------e-'},
    #         {'guess': 'i', 'result': '!'},
    #     ])
    #     potentials = opponent.get_potentials(words, opponent.get_response, game_log)
    #
    #     strategy = player.build_strategy(info_focus=1.0, success_focus=0.0, final_word_guess=True, use_cache=True)
    #     next_guess = strategy(potentials, game_log)
    #     next_guess = strategy(potentials, game_log)
    #     self.assertEqual(next_guess, 'hi')
    #
    #     self.assertEqual(get_next_guess.call_count, 1)
