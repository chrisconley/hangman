import string

MAX_WORD_GUESSES = 5
GUESS_PENALTY = 1
MAX_PENALTY = 25

class Game:
    def __init__(self, word):
        """docstring for __init__"""
        self.word = list(word)
        self.current_guess = ['-' for letter in word]
        self.score = 0
        self.known_letters = []
        self.missed_letters = []
        self.guessed_words = []

    def process_letter_guess(self, guess):
        self.score += GUESS_PENALTY
        if guess in self.word:
            self.known_letters.append(guess)
            self.current_guess = [(guess if guess == word_letter else '-') for word_letter in self.word]
        else:
            self.missed_letters.append(guess)

    def process_word_guess(self, guess):
        self.score += GUESS_PENALTY
        self.guessed_words.append(guess)
        if guess == self.word:
            self.current_guess = self.word
        elif self.lost():
            self.score = MAX_PENALTY

    def won(self):
        self.current_guess == self.word

    def lost(self):
        len(self.guessed_words) >= MAX_WORD_GUESSES

    def ended(self):
        self.won() or self.lost()

    def to_s(self):
        template = string.Template("${current_guess} | ${missed_letters} | ${guessed_words} | ${score}")
        return template.substitute(self.__dict__)


if __name__ == '__main__':

    g = Game('hello')
    print g.word
    print g.score

    g.process_letter_guess('a')

    print g.known_letters
    print g.score
    print g.to_s()

    g.process_letter_guess('e')

    print g.known_letters
    print g.score
    print g.to_s()
    print g.lost()

