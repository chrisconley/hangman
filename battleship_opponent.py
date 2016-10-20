class BattleShipGameState(str):
    """
    Accepts a word and guesses (either letter or word guesses)

    This class inherits from str, so the initializer
    returns a string in the form of:

    `10-0-0` where the "word" is `101000` and guess positions include {0, 1, 3, 5}
    """
    def __new__(cls, word, guesses, delimiter='-'):
        result = [
            (letter if (index in guesses) else delimiter)
            for index, letter
            in enumerate(word)]
        match = ''.join(result)
        obj = str.__new__(cls, match)
        obj.word = word
        obj.guesses = guesses
        return obj

    @property
    def has_sunk_all(self):
        ship_locations = len([l for l in self.word if l == '1'])
        sunk_ships = len([l for l in self if l == '1'])
        return ship_locations == sunk_ships


def play(word):
    result = BattleShipGameState(word, set())
    while True:
        if result == word or result.has_sunk_all:
            break
        next_guess = (yield result)
        if next_guess is not None:
            new_guesses = result.guesses | set([next_guess])
            print(new_guesses)
            result = BattleShipGameState(word, new_guesses)
