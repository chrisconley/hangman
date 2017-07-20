import random
import unittest

from battleship import generate, play, player
from battleship.generate import Board, Ship


class BattleshipPlayTests(unittest.TestCase):

    def test_play(self):
        random.seed(154333)
        boards = generate.run(ship_lengths=[2], size=[2, 2])
        actual_board = Board(size=[2, 2])
        actual_board.place_ship([0, 0], 2, 'H')
        assert boards[0] == actual_board
        word, game_log = play.play(actual_board, player.get_next_random_guess, boards)
        self.assertEqual(word, actual_board)
        self.assertEqual(game_log, [
            {'guess': [1, 0], 'result': None},
            {'guess': [0, 0], 'result': None},
            {'guess': [0, 1], 'result': None},
            {'guess': [1, 1], 'result': None},
            {'guess': None, 'result': None}
        ])

