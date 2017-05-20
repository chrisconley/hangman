import unittest

from hang import opponent, player, play


class HangmanPlayerTests(unittest.TestCase):
    def test_get_potentials(self):
        words = ['cat', 'bat']
        potentials = player.get_potentials(words, opponent.get_response, play.GameLog())
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

    def test_get_next_guess_naive(self):
        potentials = player.Potential({
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
        next_guess = player.get_next_guess_naive(potentials, play.GameLog())
        self.assertEqual(next_guess, 'a')

    def test_get_next_guess_naive_with_game_log(self):
        potentials = player.Potential({
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
        game_log = play.GameLog([{'guess': 'a', 'result': '-a-'}])
        next_guess = player.get_next_guess_naive(potentials, game_log)
        self.assertEqual(next_guess, 't')

    def test_get_next_guess_naive_with_one_word_left(self):
        potentials = player.Potential({
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
        game_log = play.GameLog([{'guess': 'a', 'result': '-a-'}])
        next_guess = player.get_next_guess_naive(potentials, game_log)
        self.assertEqual(next_guess, 'bat')
