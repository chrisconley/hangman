import unittest

import mastermind


class MasterMindTests(unittest.TestCase):

    def test_play(self):
        words = ['YYY', 'YYR', 'YRY', 'RYY', 'YRR', 'RYR', 'RRY', 'RRR']
        word, game_log = mastermind.play('YRY', mastermind.get_next_guess, words)
        self.assertEqual(word, 'YRY')
        self.assertEqual(game_log, [
            {'guess': 'RRY', 'result': 'BB'},
            {'guess': 'RYY', 'result': 'BWW'},
            {'guess': 'YRY', 'result': 'BBB'}
        ])

