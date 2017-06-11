import unittest

from games.hangman import opponent


class HangmanOpponentTests(unittest.TestCase):
    def test_get_response(self):
        opponent.clear_cache()
        result = opponent.get_response('cat', 't')
        self.assertEqual(result, '--t')

        opponent.clear_cache()
        result = opponent.get_response('cat', 's')
        self.assertEqual(result, '!')

        opponent.clear_cache()
        result = opponent.get_response('cat', 'cat')
        self.assertEqual(result, 'cat')

        opponent.clear_cache()
        result = opponent.get_response('cat', 'can')
        self.assertEqual(result, '!')

