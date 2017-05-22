import unittest

from battleship import generate


class GenerateTests(unittest.TestCase):
    def test_run(self):
        board = generate.Board(size=(3, 3))
        result = generate.run(ships=(2, 2), board=board)
        self.assertEqual(result, [])
