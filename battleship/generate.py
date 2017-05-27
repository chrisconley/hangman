import itertools
import random

import numpy as np


def multiset_permutations(iterable):
    """
    Ineffecient, but simple implementation, which is okay for our use case.
    Efficient implementation mentioned here: https://stackoverflow.com/a/21284776/67184
    """
    perms = itertools.permutations(iterable)
    uniq_perms = set(perms)
    return sorted([list(u) for u in uniq_perms])


class Board(object):
    def __init__(self, size):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self._board = None
        self._layout = np.zeros(self.width * self.height, dtype='int8')
        self._ships = []
        pass

    def __hash__(self):
        h = hash((
            'w{}'.format(self.width),
            'h{}'.format(self.height)
        ))
        for ship in self._ships:
            h ^= hash('r{};c{};l{};o{}'.format(ship.position[0], ship.position[1], ship.length, ship.orientation))
        return h

    def __eq__(self, other):
        return hash(self) == hash(other)

    @property
    def ships(self):
        return self._ships

    @property
    def num_ships(self):
        return len(self._ships)

    def place_ship(self, position, length, orientation):
        """
        Return None if ship cannot be placed
        """
        ship = None
        if orientation == 'H':
            zeros = np.zeros(self.width * self.height, dtype='int8')
            if (position[0] + length) > self.width:
                return None
            for i in range(length):
                zeros[position[1] * self.width + position[0]+i] = 1
            if np.all(np.bitwise_and(self._layout, zeros) == 0):
                self._layout = np.bitwise_or(self._layout, zeros)
                ship = Ship(position, length, orientation)
        elif orientation == 'V':
            zeros = np.zeros(self.width * self.height, dtype='int8')
            if (position[1] + length) > self.height:
                return None
            for i in range(length):
                zeros[(position[1] + i) * self.width + position[0]] = 1
            if np.all(np.bitwise_and(self._layout, zeros) == 0):
                self._layout = np.bitwise_or(self._layout, zeros)
                ship = Ship(position, length, orientation)
        if ship:
            self._ships.append(ship)
            return ship

    def get_next_position(self, start_position):
        start_column, start_row = start_position
        # Handle invalid inputs
        if start_column >= self.width or start_row >= self.height:
            raise RuntimeError('start_position is out of bounds')

        # The start_position is the last position on the board
        if start_column == self.width - 1 and start_row == self.height - 1:
            return None

        # We're on the last column
        elif start_column == self.width - 1:
            # Move down a row, and set column to 0
            return [0, start_row + 1]

        else:
            # Move over a column, stay on same row
            return [start_column + 1, start_row]

    def get_next_available_position(self, start_position):
        next_position = self.get_next_position(start_position)
        while next_position:
            if self.layout[next_position[1]][next_position[0]] == 0:
                return next_position
            else:
                next_position = self.get_next_position(next_position)

    @property
    def layout(self):
        return np.reshape(self._layout, (self.height, self.width)).tolist()


class Ship(object):
    def __init__(self, position, length, orientation):
        self.position = position
        self.length = length
        self.orientation = orientation

    @property
    def is_horizontal(self):
        return self.orientation == 'H'


# https://oeis.org/search?q=2%2C44%2C224%2C686%2C1622&language=english&go=Search
def run_random(ship_lengths, size, iterations=1000):
    boards = set()
    for iteration in range(iterations):
        board = Board(size=size)
        random.shuffle(ship_lengths)
        for ship_length in ship_lengths:
            placed_ship = None
            while placed_ship is None:
                row = random.randint(0, size[0]-1)
                column = random.randint(0, size[1]-1)
                orientation = random.choice(['H', 'V'])
                placed_ship = board.place_ship([row, column], ship_length, orientation)
        boards.add(board)
    return boards


def run(ship_lengths, size):
    boards = []
    orders = multiset_permutations(ship_lengths)
    for ordered_ship_lengths in orders:
        current_board = Board(size=size)
        next_ship = Ship([0, 0], ordered_ship_lengths[0], 'H')
        while True:
            placed_ship = current_board.place_ship(next_ship.position, next_ship.length, next_ship.orientation)
            if placed_ship is None:
                if next_ship.orientation == 'H':
                    next_ship = Ship(next_ship.position, next_ship.length, 'V')
                else:
                    next_position = current_board.get_next_available_position(next_ship.position)
                    if next_position is None:
                        # If we haven't been able to place any ship
                        if current_board.num_ships == 0:
                            raise 'We should never get here'
                        else:
                            current_board, next_ship = _reset_board(current_board)
                    else:
                        next_ship = Ship(next_position, next_ship.length, 'H')

            # ship was placed and we have more to place
            elif current_board.num_ships < len(ordered_ship_lengths):

                # Get the next ship length based on how many ships we've placed
                next_ship_index = current_board.num_ships
                next_ship_length = ordered_ship_lengths[next_ship_index]

                # Get the next available position based on the placed ship's position
                next_position = current_board.get_next_available_position(placed_ship.position)
                if next_position is None:
                    # If our board has only one ship and we can't find an available
                    # position, then we're done
                    if current_board.num_ships == 1:
                        break
                    # Otherwise, we need to reset the board (which removes the last ship)
                    # and continue to next iteration
                    else:
                        current_board, next_ship = _reset_board(current_board)
                        continue

                # Set the next ship
                next_ship = Ship(next_position, next_ship_length, 'H')

            # ship was placed and it was the last ship to be placed
            else:
                # add completed board
                boards.append(current_board)

                current_board, next_ship = _reset_board(current_board)

    return boards


def _reset_board(current_board):
    # Since we're starting over, before we clear the board,
    # let's get all the ships.
    current_ships = current_board.ships
    last_ship = current_ships[-1]

    # Reset current board
    current_board = Board(size=current_board.size)

    # Re-place all ships except the last one
    for ship in current_ships[:-1]:
        current_board.place_ship(ship.position, ship.length, ship.orientation)

    # Move the last ship to the next available position on the new board
    # based on where it was previously
    if last_ship.orientation == 'H':
        next_orientation = 'V'
        next_position = last_ship.position
    else:
        next_orientation = 'H'
        next_position = current_board.get_next_available_position(last_ship.position)
        # If we're not able to get a next location for the last ship,
        # then reset the board again.
        if next_position is None:
            return _reset_board(current_board)

    # Set the next ship to the next position
    next_ship = Ship(next_position, last_ship.length, next_orientation)
    return current_board, next_ship
