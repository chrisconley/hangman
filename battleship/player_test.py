import random
import unittest

from battleship import generate, player


class BattleshipPlayerTests(unittest.TestCase):
    def test_get_next_random_guess(self):
        boards = generate.run(ship_lengths=[2], size=[2, 2])
        actual_board = generate.Board(size=[2, 2])
        actual_board.place_ship([0, 0], 2, 'H')
        assert boards[0] == actual_board

        random.seed(154333)
        next_guess, _ = player.get_next_random_guess(boards, [])
        self.assertEqual(next_guess, [1, 0])

        next_guess, _ = player.get_next_random_guess(boards, [])
        self.assertEqual(next_guess, [0, 0])

    def test_get_next_random_guess_with_previous_guesses(self):
        boards = generate.run(ship_lengths=[2], size=[2, 2])
        actual_guesses = set()
        for _ in range(100):
            next_guess, _ = player.get_next_random_guess(boards, [
                {'guess': [0, 1]}
            ])
            actual_guesses.add(tuple(next_guess))

        self.assertEqual(actual_guesses, {
            (0, 0), (1, 0), (1, 1)
        })

    def test_get_next_random_guess_with_no_more_guesses(self):
        boards = generate.run(ship_lengths=[2], size=[2, 2])
        next_guess, _ = player.get_next_random_guess(boards, [
            {'guess': [0, 0]},
            {'guess': [0, 1]},
            {'guess': [1, 0]},
            {'guess': [1, 1]},
        ])
        self.assertIsNone(next_guess)

