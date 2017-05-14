class GameState(str):
    """
    Accepts a word and guesses (either letter or word guesses)

    This class inherits from str, so the initializer
    returns a string in the form of:

    `ba-a-a` where the word is `banana` and guesses include `b` and `a`
    """
    def __new__(cls, word, guesses, delimiter='-'):
        result = [
            (letter if (letter in guesses or word in guesses) else delimiter)
            for index, letter
            in enumerate(word)]
        match = ''.join(result)
        obj = str.__new__(cls, match)
        obj.word = word
        obj.guesses = guesses
        obj.delimiter = delimiter
        return obj

    @property
    def guessed_words(self):
        return {guess for guess in self.guesses if len(guess) == len(self.word)}

    @property
    def missed_words(self):
        return {guess for guess in self.guessed_words if guess != self.word}

    @property
    def guessed_letters(self):
        return self.guesses - self.guessed_words

    @property
    def known_letters(self):
        return {letter for letter in self.guessed_letters if letter in self.word}

    @property
    def missed_letters(self):
        return self.guessed_letters - self.known_letters


def apply_guess(game_state, next_guess):
    return GameState(
        word=game_state.word,
        guesses=(set(game_state.guesses) | set([next_guess])),
        delimiter=game_state.delimiter
    )


def play(word, get_next_guess, encoded_dictionary):
    game_log = []
    game_state = GameState(word, set())
    while True:
        next_guess = get_next_guess(game_state, encoded_dictionary)
        game_state = apply_guess(game_state, next_guess)
        game_log.append({
            'guess': next_guess,
            'result': (next_guess in game_state.known_letters or next_guess == word)  # TODO: word guesses?
        })
        if game_state == word:
            break

    return game_state, game_log
