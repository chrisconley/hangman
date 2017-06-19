import random
import unittest

from games import play, code_words
from games.mastermind import player, opponent, word_generator


class MastermindPlayTests(unittest.TestCase):
    def setUp(self):
        play.GUESS_CACHE = {}

    def test_play_short(self):
        words = code_words.Dictionary(['YYY', 'YYR', 'YRY', 'RYY', 'YRR', 'RYR', 'RRY', 'RRR'])
        word, game_log = play.play(
            'YRY',
            words,
            opponent.get_potentials,
            player.build_strategy(info_focus=1.0, success_focus=0.0, minimax_focus=0.0),
            opponent.get_response,
            opponent.GameLog(),
        )

        self.assertEqual(word, 'YRY')
        self.assertEqual(game_log, [
            {'guess': 'RRY', 'result': 'BB'},
            {'guess': 'RYY', 'result': 'BWW'},
            {'guess': 'YRY', 'result': 'BBB'},
        ])

        word, game_log = play.play(
            'RRR',
            words,
            opponent.get_potentials,
            player.build_strategy(info_focus=1.0, success_focus=0.0, minimax_focus=0.0),
            opponent.get_response,
            opponent.GameLog(),
        )

        self.assertEqual(word, 'RRR')
        self.assertEqual(game_log, [
            {'guess': 'RRY', 'result': 'BB'},
            {'guess': 'RYY', 'result': 'B'},
            {'guess': 'RRR', 'result': 'BBB'},
        ])

    def test_play_entropy(self):
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)
        word, game_log = play.play(
            '3632',
            dictionary,
            opponent.get_potentials,
            player.build_strategy(info_focus=1.0, success_focus=0.0, minimax_focus=0.0),
            opponent.get_response,
            opponent.GameLog(),
        )

        self.assertEqual(word, '3632')
        self.assertEqual(game_log, [
            {'guess': '1234', 'result': 'BW'},
            {'guess': '1356', 'result': 'WW'},
            {'guess': '6223', 'result': 'WWW'},
            {'guess': '1115', 'result': ''},
            {'guess': '3632', 'result': 'BBBB'},
        ])

    def test_play_minimax(self):
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)
        word, game_log = play.play(
            '3632',
            dictionary,
            opponent.get_potentials,
            player.build_strategy(info_focus=0.0, success_focus=0.0, minimax_focus=1.0),
            opponent.get_response,
            opponent.GameLog(),
        )

        self.assertEqual(word, '3632')
        self.assertEqual(game_log, [
            {'guess': '1122', 'result': 'B'},
            {'guess': '1344', 'result': 'W'},
            {'guess': '1525', 'result': 'W'},
            {'guess': '1633', 'result': 'BBW'},
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
