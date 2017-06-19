import random
import unittest

from games import play, code_words
from games.mastermind import player, opponent, word_generator


class MastermindPlayTests(unittest.TestCase):

    def test_play(self):
        random.seed(1234, version=1)
        words = code_words.Dictionary(['YYY', 'YYR', 'YRY', 'RYY', 'YRR', 'RYR', 'RRY', 'RRR'])
        word, game_log = play.play(
            'YRY',
            words,
            opponent.get_potentials,
            player.build_strategy(info_focus=1.0, success_focus=0.0, minimax_focus=0.0),
            opponent.get_response,
            opponent.GameLog(),
            use_cache=False,
        )

        self.assertEqual(word, 'YRY')
        self.assertEqual(game_log, [
            {'guess': 'YRR', 'result': 'BB'},
            {'guess': 'YRY', 'result': 'BBB'},
        ])

        word, game_log = play.play(
            'RRR',
            words,
            opponent.get_potentials,
            player.build_strategy(info_focus=1.0, success_focus=0.0, minimax_focus=0.0),
            opponent.get_response,
            opponent.GameLog(),
            use_cache=False,
        )

        self.assertEqual(word, 'RRR')
        self.assertEqual(game_log, [
            {'guess': 'RRY', 'result': 'BB'},
            {'guess': 'RYY', 'result': 'B'},
            {'guess': 'RRR', 'result': 'BBB'},
        ])

    def test_play_minimax(self):
        random.seed(12345, version=1)
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)
        word, game_log = play.play(
            '3632',
            dictionary,
            opponent.get_potentials,
            player.build_strategy(info_focus=0.0, success_focus=0.0, minimax_focus=1.0),
            opponent.get_response,
            opponent.GameLog(),
            use_cache=False,
        )

        self.assertEqual(word, '3632')
        self.assertEqual(game_log, [
            {'guess': '4433', 'result': 'BW'},
            {'guess': '6533', 'result': 'BWW'},
            {'guess': '1335', 'result': 'BW'},
            {'guess': '4532', 'result': 'BB'},
            {'guess': '3632', 'result': 'BBBB'},
        ])

        # # From http://www.cs.uni.edu/~wallingf/teaching/cs3530/resources/knuth-mastermind.pdf
        # self.assertEqual(game_log, [
        #     {'guess': '1122', 'result': 'B'},
        #     {'guess': '1344', 'result': 'W'},
        #     {'guess': '3526', 'result': 'BWW'},
        #     {'guess': '1462', 'result': 'BW'},
        #     {'guess': '3632', 'result': 'BBBB'},
        # ])
