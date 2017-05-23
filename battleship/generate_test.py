import unittest

from battleship import generate


class BoardTests(unittest.TestCase):
    def test_place_ship_horizontal(self):
        board = generate.Board(size=[3, 3])
        ship = board.place_ship((0, 0), 2, 'H')
        self.assertEqual(ship.position, (0, 0))
        self.assertEqual(ship.length, 2)
        self.assertEqual(ship.orientation, 'H')

    def test_place_ship_horizontal_overlapping(self):
        board = generate.Board(size=[4, 3])
        board.place_ship((0, 0), 2, 'H')
        ok_ship = board.place_ship((2, 0), 2, 'H')
        self.assertEqual(board.layout, [
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

        partially_overlapping_ship = board.place_ship((1, 0), 2, 'H')
        completely_overlapping_ship = board.place_ship((0, 0), 2, 'H')
        self.assertIsNotNone(ok_ship)
        self.assertIsNone(partially_overlapping_ship)
        self.assertIsNone(completely_overlapping_ship)

    def test_place_ship_horizontal_outside_right(self):
        board = generate.Board(size=[3, 3])
        ok_ship = board.place_ship((1, 0), 2, 'H')
        outside_ship = board.place_ship((2, 0), 2, 'H')
        self.assertIsNotNone(ok_ship)
        self.assertIsNone(outside_ship)
        
    def test_place_ship_vertical(self):
        board = generate.Board(size=[3, 3])
        ship = board.place_ship((0, 0), 2, 'V')
        self.assertEqual(ship.position, (0, 0))
        self.assertEqual(ship.length, 2)
        self.assertEqual(ship.orientation, 'V')

    def test_place_ship_vertical_overlapping(self):
        board = generate.Board(size=[3, 4])
        board.place_ship((0, 0), 2, 'V')
        ok_ship = board.place_ship((0, 2), 2, 'V')

        self.assertEqual(board.layout, [
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
        ])
        partially_overlapping_ship = board.place_ship((0, 1), 2, 'V')
        completely_overlapping_ship = board.place_ship((0, 0), 2, 'V')
        self.assertIsNotNone(ok_ship)
        self.assertIsNone(partially_overlapping_ship)
        self.assertIsNone(completely_overlapping_ship)

    def test_place_ship_vertical_outside_bottom(self):
        board = generate.Board(size=[3, 3])
        ok_ship = board.place_ship((0, 1), 2, 'V')
        outside_ship = board.place_ship((0, 2), 2, 'V')
        self.assertIsNotNone(ok_ship)
        self.assertIsNone(outside_ship)

    def test_num_ships_initial(self):
        board = generate.Board(size=[3, 3])
        self.assertEqual(board.num_ships, 0)

    def test_num_ships_after_placement(self):
        board = generate.Board(size=[3, 3])
        board.place_ship((0, 0), 2, 'H')
        self.assertEqual(board.num_ships, 1)

    def test_layout_initial(self):
        board = generate.Board(size=[3, 3])
        self.assertEqual(board.layout, [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])

    def test_layout_after_horizontal_placement(self):
        board = generate.Board(size=[3, 3])
        board.place_ship((0, 0), 2, 'H')
        self.assertEqual(board.layout, [
            [1, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
        ])

        board = generate.Board(size=[3, 3])
        board.place_ship((1, 1), 2, 'H')
        self.assertEqual(board.layout, [
            [0, 0, 0],
            [0, 1, 1],
            [0, 0, 0],
        ])

        board = generate.Board(size=[5, 4])
        board.place_ship((3, 2), 2, 'H')
        self.assertEqual(board.layout, [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0],
        ])

    def test_layout_after_vertical_placement(self):
        board = generate.Board(size=[3, 3])
        board.place_ship((0, 0), 2, 'V')
        self.assertEqual(board.layout, [
            [1, 0, 0],
            [1, 0, 0],
            [0, 0, 0],
        ])

        board = generate.Board(size=[3, 3])
        board.place_ship((1, 1), 2, 'V')
        self.assertEqual(board.layout, [
            [0, 0, 0],
            [0, 1, 0],
            [0, 1, 0],
        ])

        board = generate.Board(size=[4, 5])
        board.place_ship((2, 3), 2, 'V')
        self.assertEqual(board.layout, [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
        ])

    def test_get_next_position_wide_board(self):
        board = generate.Board(size=[3, 2])
        result = board.get_next_position([0, 0])
        self.assertEqual(result, [1, 0])

        result = board.get_next_position([2, 0])
        self.assertEqual(result, [0, 1])

        result = board.get_next_position([2, 1])
        self.assertEqual(result, None)

    def test_get_next_position_tall_board(self):
        board = generate.Board(size=[2, 3])
        result = board.get_next_position([0, 0])
        self.assertEqual(result, [1, 0])

        result = board.get_next_position([1, 0])
        self.assertEqual(result, [0, 1])

        result = board.get_next_position([1, 2])
        self.assertEqual(result, None)

    def test_get_next_position_invalid_inputs(self):
        board = generate.Board(size=[2, 3])
        with self.assertRaises(RuntimeError):
            board.get_next_position([2, 0])

        with self.assertRaises(RuntimeError):
            board.get_next_position([0, 3])


class GenerateTests(unittest.TestCase):
    def test_run(self):
        board = generate.Board(size=[3, 3])
        results = generate.run(ships=[2, 2], board=board)
        layouts = [b.layout for b in results]
        self.assertEqual(layouts, [1])
