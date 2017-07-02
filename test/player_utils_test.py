from decimal import Decimal
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
