import random
import unittest

from games import player_utils


class GameLog(list):
    @property
    def guesses(self):
        return {t['guess'] for t in self}


class GetNextGuessTests(unittest.TestCase):
    def test_actual_next_guess(self):
        random.seed(15243)
        choices = {
            'g': 1.75,
            't': 1.4056390622295662,
            'c': 1.4056390622295662,
            'n': 1.061278124459133,
            'u': 1.061278124459133,
            'b': 1.061278124459133,
            'l': 0.8112781244591328,
            'a': 0.8112781244591328,
            'm': 0.5435644431995964,
            'd': 0.5435644431995964,
            'o': 0.5435644431995964,
            'h': 0.5435644431995964,
            'e': 0.0,
            'r': 0.0,
            's': 0.0
        }
        next_guess = player_utils.get_actual_next_guess(choices, GameLog())
        self.assertEqual(next_guess, 'g')

    def test_actual_next_guess_tied(self):
        random.seed(15243)
        choices = {
            't': 1.4056390622295662,
            'c': 1.4056390622295662,
            'n': 1.061278124459133,
        }
        next_guess = player_utils.get_actual_next_guess(choices, GameLog())
        self.assertEqual(next_guess, 'c')

    def test_actual_next_guess_already_guessed(self):
        random.seed(15243)
        choices = {
            'b': 1,
            'n': 0.5
        }
        game_log = GameLog([{'guess': 'b'}])
        next_guess = player_utils.get_actual_next_guess(choices, game_log)
        self.assertEqual(next_guess, 'n')

    def test_actual_next_guess_no_guesses_left(self):
        random.seed(15243)
        choices = {
            'b': 1
        }
        game_log = GameLog([{'guess': 'b'}])
        next_guess = player_utils.get_actual_next_guess(choices, game_log)
        self.assertEqual(next_guess, None)

        choices = {}
        next_guess = player_utils.get_actual_next_guess(choices, GameLog())
        self.assertEqual(next_guess, None)
