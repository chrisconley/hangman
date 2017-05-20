import unittest

from hang import opponent


class HangmanOpponentTests(unittest.TestCase):
    def test_get_response(self):
        result = opponent.get_response('cat', 't')
        self.assertEqual(result, '--t')

        result = opponent.get_response('cat', 's')
        self.assertEqual(result, '!')

        result = opponent.get_response('cat', 'cat')
        self.assertEqual(result, 'cat')

        result = opponent.get_response('cat', 'can')
        self.assertEqual(result, '!')

