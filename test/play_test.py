import unittest

from games import play, code_words
from games.hangman import player, opponent


class HangmanTests(unittest.TestCase):

    def test_play(self):
        words = code_words.Dictionary(['cat', 'cot', 'can', 'car', 'bat'])
        word, game_log = play.play(
            'cat',
            words,
            opponent.get_potentials,
            player.get_next_guess_naive,
            opponent.get_response,
            opponent.GameLog()
        )

        self.assertEqual(word, 'cat')
        self.assertEqual(game_log, [
            {'guess': 'a', 'result': '-a-'},
            {'guess': 'r', 'result': '!'},
            {'guess': 'n', 'result': '!'},
            {'guess': 't', 'result': '--t'},
            {'guess': 'c', 'result': 'c--'},
            {'guess': 'cat', 'result': 'cat'},
        ])

        word, game_log = play.play(
            'cot',
            words,
            opponent.get_potentials,
            player.get_next_guess_naive,
            opponent.get_response,
            opponent.GameLog()
        )

        self.assertEqual(word, 'cot')
