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

    def test_play_entropy_alternative(self):
        random.seed(123)
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)
        word, game_log = play.play(
            '3632',
            dictionary,
            opponent.get_potentials,
            player.build_strategy(info_focus=1.0, success_focus=0.0, minimax_focus=0.0),
            opponent.get_response_alternative,
            opponent.GameLog(),
        )

        self.assertEqual(word, '3632')
        self.assertEqual(game_log, [
            {'guess': '1234', 'result': 'BW'},
            {'guess': '1356', 'result': 'WW'},
            {'guess': '2215', 'result': 'W'},
            {'guess': '3544', 'result': 'B'},
            {'guess': '3133', 'result': 'BB'},
            {'guess': '3632', 'result': 'BBBB'},
        ])

    def test_play_minimax_alternative_response(self):
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)
        word, game_log = play.play(
            '3632',
            dictionary,
            opponent.get_potentials,
            player.build_strategy(info_focus=0.0, success_focus=0.0, minimax_focus=1.0, should_sort=True),
            opponent.get_response_alternative,
            opponent.GameLog(),
        )

        self.assertEqual(word, '3632')
        self.assertEqual(game_log, [
            {'guess': '1122', 'result': 'B'},
            {'guess': '1334', 'result': 'BW'},
            {'guess': '1456', 'result': 'W'},
            {'guess': '3325', 'result': 'BWW'},
            {'guess': '3632', 'result': 'BBBB'},
        ])

    def test_play_minimax(self):
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)
        word, game_log = play.play(
            '3632',
            dictionary,
            opponent.get_minimax_potentials,
            player.build_strategy(info_focus=0.0, success_focus=0.0, minimax_focus=1.0, should_sort=True),
            opponent.get_response,
            opponent.GameLog(),
        )

        self.assertEqual(game_log, [
            {'guess': '1123', 'result': 'WW'},
            {'guess': '2432', 'result': 'BB'},
            {'guess': '3522', 'result': 'BB'},
            {'guess': '1116', 'result': 'W'},
            {'guess': '3632', 'result': 'BBBB'},
        ])

    def test_play_minimax_knuth(self):
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)

        word, game_log = play.play(
            '3632',
            dictionary,
            opponent.get_minimax_potentials,
            player.build_knuth_strategy(),
            opponent.get_response,
            opponent.GameLog(),
        )

        # From http://www.cs.uni.edu/~wallingf/teaching/cs3530/resources/knuth-mastermind.pdf
        self.assertEqual(game_log, [
            {'guess': '1122', 'result': 'B'},
            {'guess': '1344', 'result': 'W'},
            {'guess': '3526', 'result': 'BWW'},
            {'guess': '1162', 'result': 'BW'}, # In Knuth's paper, this guess is 1462
            {'guess': '3632', 'result': 'BBBB'},
        ])