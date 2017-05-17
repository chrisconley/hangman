import random
import unittest
from unittest.mock import patch

import dictionary
import hangman
import hangman_players


class HangmanPlayersTests(unittest.TestCase):
    def test_build_strategy(self):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        encoded_dictionary = dictionary.encode_dictionary(words)

        game_state = hangman.GameState('scrabbler', set('srei'))
        strategy = hangman_players.ENTROPY_ONLY
        next_guess = strategy(game_state, encoded_dictionary)

        self.assertEqual(next_guess, 'g')

        strategy = hangman_players.build_strategy(0.5, 0.5, final_word_guess=True)
        next_guess = strategy(game_state, encoded_dictionary)
        self.assertEqual(next_guess, 't')

        strategy = hangman_players.SUCCESS_ONLY
        next_guess = strategy(game_state, encoded_dictionary)
        self.assertEqual(next_guess, 'a')

    def test_build_strategy_final_word_guess(self):
        random.seed(15243)
        words = ['scrabbler']
        encoded_dictionary = dictionary.encode_dictionary(words)

        game_state = hangman.GameState('scrabbler', set('srei'))
        strategy = strategy = hangman_players.build_strategy(0.5, 0.5, final_word_guess=True)
        next_guess = strategy(game_state, encoded_dictionary)

        self.assertEqual(next_guess, 'scrabbler')

    @patch('hangman_players.dictionary.filter_words')
    def test_build_strategy_does_not_cache_counts(self, filter_words):
        filter_words.return_value = ['scrabbler', 'scrambler']
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        encoded_dictionary = dictionary.encode_dictionary(words)

        game_state = hangman.GameState('scrabbler', set('srei'))
        strategy = hangman_players.ENTROPY_ONLY
        strategy(game_state, encoded_dictionary)
        strategy(game_state, encoded_dictionary)

        self.assertEqual(filter_words.call_count, 2)

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
        game_state = hangman.GameState('scrabbler', set(''))
        next_guess = hangman_players.get_actual_next_guess(game_state, choices)
        self.assertEqual(next_guess, 'g')

    def test_actual_next_guess_tied(self):
        random.seed(15243)
        choices = {
            't': 1.4056390622295662,
            'c': 1.4056390622295662,
            'n': 1.061278124459133,
        }
        game_state = hangman.GameState('scrabbler', set(''))
        next_guess = hangman_players.get_actual_next_guess(game_state, choices)
        self.assertEqual(next_guess, 'c')

    def test_actual_next_guess_already_guessed(self):
        random.seed(15243)
        choices = {
            'b': 1.4056390622295662,
            'n': 1.061278124459133,
        }
        game_state = hangman.GameState('scrabbler', set('b'))
        next_guess = hangman_players.get_actual_next_guess(game_state, choices)
        self.assertEqual(next_guess, 'n')

    def test_actual_next_guess_no_guesses_left(self):
        random.seed(15243)
        choices = {
            'b': 1.4056390622295662,
        }
        game_state = hangman.GameState('scrabbler', set('b'))
        next_guess = hangman_players.get_actual_next_guess(game_state, choices)
        self.assertEqual(next_guess, None)