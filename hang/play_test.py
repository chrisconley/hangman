import unittest

from hang import play, player, opponent


class HangmanTests(unittest.TestCase):

    def test_play(self):
        words = ['cat', 'cot', 'can', 'car', 'bat']
        word, game_log = play.play(
            'cat',
            words,
            player.get_potentials,
            player.get_next_guess_naive,
            opponent.get_response
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

