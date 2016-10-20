import random
import unittest

import hangman
from hangman_utils import counters
import play
import scorers


class NextGuessTests(unittest.TestCase):

    def test_max_info_gain(self):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        counts = counters.count_positional_letters(words)
        scorer = scorers.build_multiplier_scorer(1, 1)
        game_state = hangman.HangmanGameState('scrabbler', 'srei')
        next_guess = play.entropy_strategy(game_state, counts, len(words), scorer)

        self.assertEqual(next_guess, 'g')

        scorer = scorers.build_multiplier_scorer(0, 1)
        next_guess = play.entropy_strategy(game_state, counts, len(words), scorer)

        self.assertEqual(next_guess, 't')

        next_guess = play.most_common_strategy(game_state, counts, len(words), scorer)
        self.assertEqual(next_guess, 'a')

    def test_next_guess(self):
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
        game_state = hangman.HangmanGameState('scrabbler', '')
        next_guess = play.get_actual_next_guess(game_state, choices)
        self.assertEqual(next_guess, 'g')

    def test_tied_next_guess(self):
        random.seed(15243)
        choices = {
            't': 1.4056390622295662,
            'c': 1.4056390622295662,
            'n': 1.061278124459133,
        }
        game_state = hangman.HangmanGameState('scrabbler', '')
        next_guess = play.get_actual_next_guess(game_state, choices)
        self.assertEqual(next_guess, 'c')

    def test_already_guessed_next_guess(self):
        random.seed(15243)
        choices = {
            'b': 1.4056390622295662,
            'n': 1.061278124459133,
        }
        game_state = hangman.HangmanGameState('scrabbler', 'b')
        next_guess = play.get_actual_next_guess(game_state, choices)
        self.assertEqual(next_guess, 'n')
