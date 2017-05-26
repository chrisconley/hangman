import numpy as np


class Board(object):
    def __init__(self, size):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self._board = None
        self._layout = np.zeros(self.width * self.height, dtype='int8')
        self._ships = []
        pass

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


def run(ship_lengths, size):
    current_board = Board(size=size)
    boards = []
    next_ship = Ship([0, 0], ship_lengths[0], 'H')
    while True:
        placed_ship = current_board.place_ship(next_ship.position, next_ship.length, next_ship.orientation)
        if placed_ship is None:
            if next_ship.orientation == 'H':
                next_ship = Ship(next_ship.position, next_ship.length, 'V')
            else:
                next_position = current_board.get_next_available_position(next_ship.position)
                if next_position is None:

                    # If we haven't been able to place any ship, then exit
                    # NB: Not entirely confident this is correct logic
                    if current_board.num_ships == 0:
                        # print('exiting')
                        break
                    else:
                        current_board, next_ship = _reset_board(current_board)
                else:
                    next_ship = Ship(next_position, next_ship.length, 'H')

        # ship was placed and we have more to place
        elif current_board.num_ships < len(ship_lengths):

            # Get the next ship length based on how many ships we've placed
            next_ship_index = current_board.num_ships
            next_ship_length = ship_lengths[next_ship_index]

            # Get the next available position based on the placed ship's position
            next_position = current_board.get_next_available_position(placed_ship.position)
            if next_position is None:
                # If our board has only one ship and we can't find an available
                # position, then we're done
                if current_board.num_ships == 1:
                    break
                else:
                    raise 'Hi again'

            # Set the next ship
            next_ship = Ship(next_position, next_ship_length, 'H')

        # ship was placed and it was the last ship to be placed
        else:
            # add completed board
            boards.append(current_board)

            # print('Appended board:')
            # for row in current_board.layout:
            #     print(row)

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

    # print('Newly constructed board')
    # for row in current_board.layout:
    #     print(row)

    # Move the last ship to the next available position on the new board
    # based on where it was previously
    if last_ship.orientation == 'H':
        next_orientation = 'V'
        next_position = last_ship.position
    else:
        next_orientation = 'H'
        next_position = current_board.get_next_available_position(last_ship.position)
        if next_position is None:
            raise 'Hi once again'

    # Set the next ship to the next position
    next_ship = Ship(next_position, last_ship.length, next_orientation)
    return current_board, next_ship


def runx(ship_lengths, size):
    """
    If we're ready for next iteration,
      a) If ship is horizontal, switch to vertical and call run
      b) If ship is vertical, switch to horizontal and move one space forward

    Edge cases:
      What do we do when b) puts us off the last position of the board
      How do we handle ships that can't be place anywhere
    """
    moving_ship_index = 0
    first_ship_position = [0, 0]
    moving_ship_position = [0, 0]
    moving_ship_orientation = 'H'
    placed_attempts = 0
    current_board = Board(size=size)
    boards = []
    while True:
        moving_ship_length = ship_lengths[moving_ship_index]
        moving_ship_length = ship_lengths[moving_ship_index]
        placed_ship = current_board.place_ship(moving_ship_position, moving_ship_length, moving_ship_orientation)
        placed_attempts += 1
        if placed_ship is None:
            # If it's orientation is 'H', we'll try next time with 'V'
            if moving_ship_orientation == 'H':
                moving_ship_orientation = 'V'
                placed_attempts -= 1
                moving_ship_index -= 1
            # If it's the first ship and orientation is 'V', we know we're done
            elif moving_ship_index == 0 and moving_ship_orientation == 'V':
                break
            # If it's any other ship and orientation is 'V', we move up the index
            # and go back to 'H' orientation
            elif placed_ship is None and moving_ship_orientation == 'V':
                moving_ship_index -= 2
                moving_ship_orientation = 'H'
                placed_attempts -= 1
            else:
                raise 'wat'
        else:
            moving_ship_position = current_board.get_next_available_position(moving_ship_position)
            moving_ship_index += 1
            moving_ship_orientation = 'H'

        if placed_attempts == ship_lengths:
            if current_board.num_ships == ship_lengths:
                boards.append(current_board)
            current_board = Board(size=size)
            moving_ship_index = 0
            moving_ship_position = current_board.get_next_position(first_ship_position)
            moving_ship_orientation = 'H'
            placed_attempts = 0
            continue


    return boards


def _run(desired_num_ships, ships_to_be_placed, ships_already_placed, board, current_ship):

    # If we've placed all ships, return the board
    if board.num_ships == desired_num_ships:
        return [board]

    next_position = board.get_next_position(current_ship.position)

    # If we haven't placed all ships, and we're at the end of the board,
    # Then we haven't been about to place all ships
    if next_position is None:
        return []

    return _run(desired_num_ships, ships_to_be_placed, ships_already_placed, board, current_ship)











    # If we haven't been able to place all ships, then exit out
    # if board.num_ships != desired_num_ships and len(ships_to_be_placed) == 0:
    #     return []

    # If we still need to place more ships
    if len(ships_to_be_placed) >= 1:
        next_position = board.get_next_position(current_ship.position)
        next_ship = Ship(next_position, ships_to_be_placed[0], 'H')
        return [board] + _run(desired_num_ships, ships_to_be_placed[1:], ships_already_placed, board, next_ship)

    next_position = board.get_next_position(current_ship.position)
    if current_ship.is_horizontal:
        return [board] + _run(desired_num_ships, ships_to_be_placed, ships_already_placed, board, current_ship)
    elif next_position is None: # we've reached end of board and haven't been able to place all ships
        return []
    else:
        next_ship = Ship(next_position, current_ship.length, 'H')
        return [board] + _run(desired_num_ships, ships_to_be_placed, ships_already_placed, board, current_ship)
    # if current_ship:
    #     _run(ships_to_be_placed[1:], ships_already_placed.append(current_ship), board)