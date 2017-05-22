
class Board(object):
    def __init__(self, size=(3,3)):
        self._board = None
        pass

    @property
    def num_ships(self):
        return len(self._ships)

    def place_ship(self, position, length, orientation):
        """
        Return None if ship cannot be placed
        """
        self._board
        pass


class Ship(object):
    def __init__(self, position, length, orientation):
        self.position = position
        self.length = length
        self.orientation = orientation

    @property
    def is_horizontal(self):
        return self.orientation == 'H'


def run(ships, board):
    """
    If we're ready for next iteration,
      a) If ship is horizontal, switch to vertical and call run
      b) If ship is vertical, switch to horizontal and move one space forward

    Edge cases:
      What do we do when b) puts us off the last position of the board
      How do we handle ships that can't be place anywhere
    """
    current_ship = Ship((0,0), ships[0], 'H')
    return _run(
        desired_num_ships=len(ships),
        ships_to_be_placed=ships,
        ships_already_placed=[],
        board=board,
        current_ship=current_ship)


def _run(desired_num_ships, ships_to_be_placed, ships_already_placed, board, current_ship):

    placed_ship = board.place_ship(current_ship.position, current_ship.length, current_ship.orientation)

    if placed_ship is None:  # we couldn't place ship
        return None

    # If we've placed all ships, return the board
    if board.num_ships == desired_num_ships:
        return board

    # If we have been able to place all ships, then exit out
    if board.num_ships != desired_num_ships and len(ships_to_be_placed) == 0:
        return None

    # If we still need to place more ships
    if len(ships_to_be_placed) >= 1:
        next_position = board.get_next_position(current_ship.position)
        next_ship = Ship(next_position, ships_to_be_placed[1:], 'H')
        return _run(desired_num_ships, ships_to_be_placed[1:], ships_already_placed, board, next_ship)

    next_position = board.get_next_position(current_ship.position)
    if current_ship.is_horizontal:
        return _run(desired_num_ships, ships_to_be_placed, ships_already_placed, board, current_ship)
    elif next_position is None: # we've reached end of board and haven't been able to place all ships
        return None
    else:
        next_ship = Ship(next_position, current_ship.length, 'H')
        return _run(desired_num_ships, ships_to_be_placed, ships_already_placed, board, current_ship)
    # if current_ship:
    #     _run(ships_to_be_placed[1:], ships_already_placed.append(current_ship), board)