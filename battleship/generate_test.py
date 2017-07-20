import unittest

from battleship import generate


class MultiSetPermutationTests(unittest.TestCase):
    def test_multiset_permutations_length_2(self):
        result = generate.multiset_permutations([1, 1])
        self.assertEqual(result, [
            [1, 1]
        ])

        result = generate.multiset_permutations([2, 1])
        self.assertEqual(result, [
            [1, 2],
            [2, 1],
        ])

    def test_multiset_permutations_length_3(self):
        result = generate.multiset_permutations([1, 1, 1])
        self.assertEqual(result, [
            [1, 1, 1]
        ])

        result = generate.multiset_permutations([1, 1, 2])
        self.assertEqual(result, [
            [1, 1, 2],
            [1, 2, 1],
            [2, 1, 1],
        ])

        result = generate.multiset_permutations([1, 2, 3])
        self.assertEqual(result, [
            [1, 2, 3],
            [1, 3, 2],
            [2, 1, 3],
            [2, 3, 1],
            [3, 1, 2],
            [3, 2, 1],
        ])


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

    def test_get_next_position_next_row(self):
        board = generate.Board(size=[3, 3])
        board.place_ship((0, 0), 2, 'H')

        result = board.get_next_position([2, 0])
        self.assertEqual(result, [0, 1])

        result = board.get_next_position([0, 2])
        self.assertEqual(result, [1, 2])

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

        self.assertEqual(board.layout, [
            [0, 0],
            [0, 0],
            [0, 0],
        ])
        with self.assertRaises(RuntimeError):
            board.get_next_position([2, 0])

        with self.assertRaises(RuntimeError):
            board.get_next_position([0, 3])

    def test_get_next_available_position_horizontal(self):
        # No previous ships placed
        board = generate.Board(size=[3, 2])
        result = board.get_next_available_position([0, 0])
        self.assertEqual(result, [1, 0])

        # Same Row
        board = generate.Board(size=[3, 3])
        board.place_ship((0, 0), 2, 'H')
        result = board.get_next_available_position([0, 0])
        self.assertEqual(result, [2, 0])

        # Crosses Row
        # [
        #     [0, 1, 1],
        #     [1, 1, 0],
        #     [0, 0, 0]
        # ]
        board = generate.Board(size=[3, 3])
        board.place_ship((1, 0), 2, 'H')
        board.place_ship((0, 1), 2, 'H')
        result = board.get_next_available_position([2, 0])
        self.assertEqual(result, [2, 1])

        # No available positions
        # [
        #     [0, 0, 0],
        #     [0, 0, 0],
        #     [0, 1, 1]
        # ]
        board = generate.Board(size=[3, 3])
        board.place_ship((1, 2), 2, 'H')

        result = board.get_next_available_position([1, 2])
        self.assertEqual(result, None)


class GenerateTests(unittest.TestCase):
    def test_run_2_2_on_2x2(self):
        results = generate.run(ship_lengths=[2, 2], size=[2, 2])
        layouts = [b.layout for b in results]

        self.assertEqual(len(layouts), 2)

        # both ships horizontal
        self.assertEqual(layouts[0], [
            [1, 1],
            [1, 1]])

        # both ships vertical
        self.assertEqual(layouts[1], [
            [1, 1],
            [1, 1]])

    def test_run_2_2_on_3x3(self):
        results = generate.run(ship_lengths=[2, 2], size=[3, 3])
        layouts = [b.layout for b in results]

        self.assertEqual(len(layouts), 44)

        self.assertEqual(layouts[0], [
            [1, 1, 1],
            [0, 0, 1],
            [0, 0, 0]])

        self.assertEqual(layouts[-1], [
            [0, 0, 0],
            [0, 0, 1],
            [1, 1, 1]])

    def test_run_2_2_on_4x4(self):
        results = generate.run(ship_lengths=[2, 2], size=[4, 4])
        layouts = [b.layout for b in results]

        self.assertEqual(len(layouts), 224)

    def test_run_2_2_on_5x5(self):
        results = generate.run(ship_lengths=[2, 2], size=[5, 5])
        layouts = [b.layout for b in results]

        self.assertEqual(len(layouts), 686)

    def test_run_2_2_3_on_4x4(self):
        boards = generate.run(ship_lengths=[2, 3, 2], size=[4, 4])
        self.assertEqual(len(boards), 1600)

    def test_run_random_3_2_1_on_4x4(self):
        boards = generate.run(ship_lengths=[3, 2, 1], size=[4, 4])
        self.assertEqual(len(boards), 5808)

    def test_run_random_2_2_3_on_5x5(self):
        boards = generate.run(ship_lengths=[2, 2, 3], size=[5, 5])
        self.assertEqual(len(boards), 12798)

    @unittest.skip('Takes >5 minutes to run')
    def test_run_large_board(self):
        results = generate.run(ship_lengths=[1, 2, 3, 4], size=[6, 6])
        self.assertEqual(len(results), 2895696)

    def test_run_random_2_2_on_2x2(self):
        boards = generate.run_random(ship_lengths=[2, 2], size=[2, 2])
        self.assertEqual(len(boards), 2)

    def test_run_random_2_2_on_3x3(self):
        boards = generate.run_random(ship_lengths=[2, 2], size=[3, 3], iterations=10000)
        self.assertEqual(len(boards), 44)

    @unittest.skip('No need to run these lengthy tests now that we have the number')
    def test_run_random_2_2_on_4x4(self):
        boards = generate.run_random(ship_lengths=[2, 2], size=[4, 4], iterations=100000)
        self.assertEqual(len(boards), 224)

    @unittest.skip('No need to run these lengthy tests now that we have the number')
    def test_run_random_2_2_on_5x5(self):
        boards = generate.run_random(ship_lengths=[2, 2], size=[5, 5], iterations=100000)
        self.assertEqual(len(boards), 686)

    @unittest.skip('No need to run these lengthy tests now that we have the number')
    def test_run_random_2_2_on_6x6(self):
        boards = generate.run_random(ship_lengths=[2, 2], size=[6, 6], iterations=100000)
        self.assertEqual(len(boards), 1622)

    @unittest.skip('No need to run these lengthy tests now that we have the number')
    def test_run_random_2_2_3_on_4x4(self):
        boards = generate.run_random(ship_lengths=[2, 2, 3], size=[4, 4], iterations=500000)
        self.assertEqual(len(boards), 1600)

    @unittest.skip('No need to run these lengthy tests now that we have the number')
    def test_run_random_2_2_3_on_4x4(self):
        boards = generate.run_random(ship_lengths=[3, 2, 1], size=[4, 4], iterations=1000000)
        self.assertEqual(len(boards), 5808)

    @unittest.skip('No need to run these lengthy tests now that we have the number')
    def test_run_random_2_2_3_on_5x5(self):
        boards = generate.run_random(ship_lengths=[2, 2, 3], size=[5, 5], iterations=500000)
        self.assertEqual(len(boards), 12798)

    @unittest.skip('No need to run these lengthy tests now that we have the number')
    def test_run_random_2_2_3_on_6x6(self):
        boards = generate.run_random(ship_lengths=[2, 2, 3], size=[6, 6], iterations=2000000)
        self.assertEqual(len(boards), 56824)
