class HangmanGameState(str):
    def __new__(cls, word, guesses, delimiter='-'):
        result = [
            (letter if (letter in guesses or word in guesses) else delimiter)
            for index, letter
            in enumerate(word)]
        match = ''.join(result)
        obj = str.__new__(cls, match)
        obj.word = word
        obj.guesses = guesses
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
