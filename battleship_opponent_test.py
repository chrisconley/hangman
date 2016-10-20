import unittest

from battleship_opponent import BattleShipGameState


class BattleShipGameStateTests(unittest.TestCase):
    def test_string(self):
        state = BattleShipGameState('101000', set())
        self.assertEqual(state, '------')

        state = BattleShipGameState('101000', set([1]))
        self.assertEqual(state, '-0----')

        state = BattleShipGameState('101000', set([0, 2, 5]))
        self.assertEqual(state, '1-1--0')

        state = BattleShipGameState('1110000000', set([0]))
        self.assertEqual(state, '1---------')
