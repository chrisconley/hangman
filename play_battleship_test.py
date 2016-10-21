import random
import unittest

import play_battleship
from battleship_opponent import BattleShipGameState


class PlayBattleShipTests(unittest.TestCase):
    def test_get_next_random_guess(self):
        random.seed(15243)
        game_state = BattleShipGameState('1110', set([1]))
        result = play_battleship.get_next_random_guess(game_state)
        self.assertEqual(result, 3)

        game_state = BattleShipGameState('1110', set([1, 3, 2]))
        result = play_battleship.get_next_random_guess(game_state)
        self.assertEqual(result, 0)

    def test_get_next_neighbor_guess_moving_from_first(self):
        # If we know first is a hit, then guess second
        game_state = BattleShipGameState('1110', set([0]))
        result = play_battleship.get_next_neighbor_guess(game_state)
        self.assertEqual(result, 1)

        # If we know second is a hit, then guess third
        game_state = BattleShipGameState('1110', set([0, 1]))
        result = play_battleship.get_next_neighbor_guess(game_state)
        self.assertEqual(result, 2)

    def test_get_next_neighbor_guess_moving_from_last(self):
        # If we know last is a hit, then guess second to last
        game_state = BattleShipGameState('0111', set([3]))
        result = play_battleship.get_next_neighbor_guess(game_state)
        self.assertEqual(result, 2)

        # If we know second to last is a hit, then guess third to last
        game_state = BattleShipGameState('0111', set([3, 2]))
        result = play_battleship.get_next_neighbor_guess(game_state)
        self.assertEqual(result, 1)

    def test_get_next_neighbor_guess_one_left(self):
        game_state = BattleShipGameState('0000', set([0, 1, 2]))
        result = play_battleship.get_next_neighbor_guess(game_state)
        self.assertEqual(result, 3)

    def test_get_next_neighbor_guess_random_first_guess(self):
        random.seed(15243)
        game_state = BattleShipGameState('0000', set([]))
        result = play_battleship.get_next_neighbor_guess(game_state)
        self.assertEqual(result, 1)

    def test_get_next_neighbor_guess_second_from_end(self):

        # Guess the last spot if we know second to last is a hit
        game_state = BattleShipGameState('0110', set([2]))
        result = play_battleship.get_next_neighbor_guess(game_state)
        self.assertEqual(result, 3)

        # Guess the first spot if we know second is a hit
        game_state = BattleShipGameState('0110', set([1]))
        result = play_battleship.get_next_neighbor_guess(game_state)
        self.assertEqual(result, 0)
