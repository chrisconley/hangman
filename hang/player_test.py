import random
import unittest

from hang import opponent, player, play


class HangmanPlayerTests(unittest.TestCase):
    def test_build_strategy(self):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        game_log = play.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r------r'},
            {'guess': 'e', 'result': '-------e-'},
            {'guess': 'i', 'result': '!'},
        ])
        potentials = player.get_potentials(words, opponent.get_response, game_log)

        strategy = player.build_strategy(info_focus=1.0, success_focus=0.0, final_word_guess=True)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'g')

        strategy = player.build_strategy(0.5, 0.5, final_word_guess=True)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 't')

        strategy = player.build_strategy(info_focus=0.0, success_focus=1.0, final_word_guess=True)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'a')

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
