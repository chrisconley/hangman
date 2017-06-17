import unittest

from games.battleship import opponent


class HangmanOpponentTests(unittest.TestCase):
    @unittest.skip('how do we return "Sink" in responses?')
    def test_get_response(self):
        result = opponent.get_response('111100000', '2')
        self.assertEqual(result, 'HitSink')

        result = opponent.get_response('111,100,000', '---------')
        result = opponent.get_response('111,100,000', '2;--XX--X--')
        result = opponent.get_response('111,100,000', 2, (1, 3, 4))
        self.assertEqual(result, 'Hit')

        result = opponent.get_response('1,0;2;H:0,0;2;V', '2')
        self.assertEqual(result, 'Miss')

        result = opponent.get_response('33102H002V', '2')
        self.assertEqual(result, 'Miss')

        ships = (
            ((1, 0), 2, 'H'),
            ((0, 0), 2, 'V'),
        )
        result = opponent.get_response(ships, '2')
        self.assertEqual(result, 'Miss')
