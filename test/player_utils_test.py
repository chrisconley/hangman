from decimal import Decimal
from unittest.mock import Mock
import numpy as np
import random
import unittest

from games import player_utils
import games.code_words


class GameLog(list):
    @property
    def guesses(self):
        return {t['guess'] for t in self}


class GetNextGuessTests(unittest.TestCase):
    def test_actual_next_guess(self):
        random.seed(15243)
        choices = {
            'g': Decimal(1.75),
            't': Decimal(1.4056390622295662),
            'c': Decimal(1.4056390622295662),
            'n': Decimal(1.061278124459133),
            'u': Decimal(1.061278124459133),
            'b': Decimal(1.061278124459133),
            'l': Decimal(0.8112781244591328),
            'a': Decimal(0.8112781244591328),
            'm': Decimal(0.5435644431995964),
            'd': Decimal(0.5435644431995964),
            'o': Decimal(0.5435644431995964),
            'h': Decimal(0.5435644431995964),
            'e': Decimal(0.0),
            'r': Decimal(0.0),
            's': Decimal(0.0),
        }
        next_guess = player_utils.get_actual_next_guess(choices, GameLog())
        self.assertEqual(next_guess, 'g')

    def test_actual_next_guess_tied(self):
        random.seed(15243)
        choices = {
            't': Decimal(1.4056390622295662),
            'c': Decimal(1.4056390622295662),
            'n': Decimal(1.061278124459133),
        }
        next_guess = player_utils.get_actual_next_guess(choices, GameLog())
        self.assertEqual(next_guess, 'c')

    def test_actual_next_guess_already_guessed(self):
        random.seed(15243)
        choices = {
            'b': Decimal(1),
            'n': Decimal(0.5),
        }
        game_log = GameLog([{'guess': 'b'}])
        next_guess = player_utils.get_actual_next_guess(choices, game_log)
        self.assertEqual(next_guess, 'n')

    def test_actual_next_guess_no_guesses_left(self):
        random.seed(15243)
        choices = {
            'b': Decimal()
        }
        game_log = GameLog([{'guess': 'b'}])
        next_guess = player_utils.get_actual_next_guess(choices, game_log)
        self.assertEqual(next_guess, None)

        choices = {}
        next_guess = player_utils.get_actual_next_guess(choices, GameLog())
        self.assertEqual(next_guess, None)


class ModelsTests(unittest.TestCase):
    def assertDecimalAlmostEqual(self, actual, expected, places):
        self.assertEqual(type(actual), Decimal)
        self.assertAlmostEqual(float(actual), float(expected), places=places)

    def setUp(self):
        self.data = {
            'info': {'g': Decimal(1.75), 't': Decimal(1.40564), 'a': Decimal(0.81128)},
            'reward': {'g': Decimal(0.5), 't': Decimal(0.625), 'a': Decimal(0.75)},
            'speed': {'g': Decimal(0.33), 't': Decimal(0.33), 'a': Decimal(0.33)},
            'minimax': {'g': Decimal(0.33), 't': Decimal(0.33), 'a': Decimal(0.33)}
        }

    def test_weighted_sum_all_info(self):
        foci = {'info': 1.0}
        results = player_utils.weighted_sum(self.data, foci)
        self.assertEqual(sorted(results.keys()), ['a', 'g', 't'])
        self.assertDecimalAlmostEqual(results['g'], Decimal(0.44115), places=5)
        self.assertDecimalAlmostEqual(results['t'], Decimal(0.35434), places=5)
        self.assertDecimalAlmostEqual(results['a'], Decimal(0.20451), places=5)

    def test_weighted_sum_all_info_zero_reward(self):
        foci = {'info': 1.0, 'reward': 0.0}
        results = player_utils.weighted_sum(self.data, foci)
        self.assertEqual(sorted(results.keys()), ['a', 'g', 't'])
        self.assertDecimalAlmostEqual(results['g'], Decimal(0.44115), places=5)
        self.assertDecimalAlmostEqual(results['t'], Decimal(0.35434), places=5)
        self.assertDecimalAlmostEqual(results['a'], Decimal(0.20451), places=5)

    def test_weighted_sum_event_info_reward_split(self):
        foci = {'info': 0.5, 'reward': 0.5}
        results = player_utils.weighted_sum(self.data, foci)
        self.assertEqual(sorted(results.keys()), ['a', 'g', 't'])
        self.assertDecimalAlmostEqual(results['g'], Decimal(0.35391), places=5)
        self.assertDecimalAlmostEqual(results['t'], Decimal(0.34384), places=5)
        self.assertDecimalAlmostEqual(results['a'], Decimal(0.30226), places=5)

    def test_weighted_product_all_info(self):
        foci = {'info': 1.0}
        results = player_utils.weighted_product(self.data, foci)
        self.assertEqual(sorted(results.keys()), ['a', 'g', 't'])
        self.assertDecimalAlmostEqual(results['g'], Decimal(1.75), places=5)
        self.assertDecimalAlmostEqual(results['t'], Decimal(1.40564), places=5)
        self.assertDecimalAlmostEqual(results['a'], Decimal(0.81128), places=5)

    def test_weighted_product_all_info_zero_reward(self):
        foci = {'info': 1.0, 'reward': 0.0}
        results = player_utils.weighted_product(self.data, foci)
        self.assertEqual(sorted(results.keys()), ['a', 'g', 't'])
        self.assertDecimalAlmostEqual(results['g'], Decimal(1.75), places=5)
        self.assertDecimalAlmostEqual(results['t'], Decimal(1.40564), places=5)
        self.assertDecimalAlmostEqual(results['a'], Decimal(0.81128), places=5)

    def test_weighted_product_event_info_reward_split(self):
        foci = {'info': 0.5, 'reward': 0.5}
        results = player_utils.weighted_product(self.data, foci)
        self.assertEqual(sorted(results.keys()), ['a', 'g', 't'])
        self.assertDecimalAlmostEqual(results['g'], Decimal(0.93541), places=5)
        self.assertDecimalAlmostEqual(results['t'], Decimal(0.93730), places=5)
        self.assertDecimalAlmostEqual(results['a'], Decimal(0.78004), places=5)

    def test_og_weighted(self):
        foci = {}
        results = player_utils.weighted_og(self.data, foci)
        self.assertEqual(sorted(results.keys()), ['a', 'g', 't'])
        self.assertDecimalAlmostEqual(results['g'], Decimal(0.875), places=5)
        self.assertDecimalAlmostEqual(results['t'], Decimal(0.87853), places=4)
        self.assertDecimalAlmostEqual(results['a'], Decimal(0.60846), places=5)

class BuildStrategyTests(unittest.TestCase):
    def test_build_strategy_with_one_word_left(self):
        strategy = player_utils.build_strategy(
            foci={},
            model=Mock('model', return_value={'g': Decimal(1.0), 't': Decimal(1.0)}),
            reward_pmf=Mock('reward_pmf', return_value={'*': Decimal(1.0), '!': Decimal(1.0)}),
            should_sort=False
        )

        potential_outcomes = games.code_words.PotentialOutcomes()
        potential_outcomes.add('c', 'c--', 'cat')
        result = strategy(potential_outcomes, GameLog)
        self.assertEqual(result, 'cat')

    def test_build_strategy_random_selection_vs_sorted(self):
        random.seed(1234)
        strategy = player_utils.build_strategy(
            foci={},
            model=Mock('model', return_value={'e': Decimal(1.0), 't': Decimal(1.0)}),
            reward_pmf=Mock('reward_pmf', return_value={'*': Decimal(1.0), '!': Decimal(1.0)}),
            should_sort=False
        )

        potential_outcomes = games.code_words.PotentialOutcomes()
        potential_outcomes.add('c', 'c--', 'cate')
        potential_outcomes.add('c', 'c--', 'cote')
        result = strategy(potential_outcomes, GameLog())
        self.assertEqual(result, 't')

        random.seed(1234)
        strategy = player_utils.build_strategy(
            foci={},
            model=Mock('model', return_value={'e': Decimal(1.0), 't': Decimal(1.0)}),
            reward_pmf=Mock('reward_pmf', return_value={'*': Decimal(1.0), '!': Decimal(1.0)}),
            should_sort=True
        )

        potential_outcomes = games.code_words.PotentialOutcomes()
        potential_outcomes.add('c', 'c--', 'cate')
        potential_outcomes.add('c', 'c--', 'cote')
        result = strategy(potential_outcomes, GameLog())
        self.assertEqual(result, 'e')


class CounterTests(unittest.TestCase):
    def assertDecimalAlmostEqual(self, actual, expected, places):
        self.assertEqual(type(actual), Decimal)
        self.assertAlmostEqual(float(actual), float(expected), places=places)

    def test_get_pmf_for_entropy(self):
        possible_responses = games.code_words.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar'}
        })
        pmf = player_utils._get_pmf_for_entropy(possible_responses)
        self.assertIsNone(pmf.get('*'))
        self.assertDecimalAlmostEqual(pmf['c--'], Decimal('0.20000000000000'), places=17)
        self.assertDecimalAlmostEqual(pmf['!'], Decimal('0.60000000000000'), places=17)

        possible_responses = games.code_words.PossibleResponses.from_dict('d', {
            '!': {'bar', 'tab', 'tar', 'ace', 'cat'}
        })
        pmf = player_utils._get_pmf_for_entropy(possible_responses)
        self.assertIsNone(pmf.get('*'))
        self.assertDecimalAlmostEqual(pmf['!'], Decimal('1.00000000000000'), places=17)

    def test_get_pmf_for_entropy_raises_if_duplicate_invalid_codewords(self):
        possible_responses = games.code_words.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace', 'cat'},
            '!': {'bar', 'tab', 'tar'}
        })
        with self.assertRaises(AssertionError):
            player_utils._get_pmf_for_entropy(possible_responses)

        possible_responses = games.code_words.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar', 'cat'}
        })
        with self.assertRaises(AssertionError):
            player_utils._get_pmf_for_entropy(possible_responses)

    def test_get_pmf_for_speed(self):
        np.random.seed(23)
        possible_responses = games.code_words.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar'}
        })
        pmf = player_utils._get_pmf_for_speed(possible_responses)
        self.assertDecimalAlmostEqual(sum(pmf.values()), Decimal('1.0'), places=3)
