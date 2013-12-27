import random

MAX_WORD_GUESSES = 5
GUESS_PENALTY = 1
MAX_PENALTY = 25
DICTIONARY = ['hello', 'cat', 'eat', 'cash', 'bet', 'ear', 'teach']

class Game(object):
    def __init__(self):
        word = random.choice(DICTIONARY)
        self._word = list(word)
        self.current_guess = ['-' for letter in word]
        self.score = 0
        self.known_letters = []
        self.missed_letters = []
        self.guessed_words = []

    def process_guess(self, guess):
        self.score += GUESS_PENALTY
        if len(guess) == 1:
            self.process_letter_guess(guess)
        else:
            self.process_word_guess(guess)

    def process_letter_guess(self, guess):
        if guess in self._word:
            self.known_letters.append(guess)
            self.current_guess = [
                (word_letter if word_letter in self.known_letters else '-')
                for word_letter
                in self._word
            ]
        else:
            self.missed_letters.append(guess)

    def process_word_guess(self, guess):
        self.guessed_words.append(guess)
        if guess == self._word:
            self.current_guess = self._word
        elif self.lost():
            self.score = MAX_PENALTY

    def play(self, player):
        while not self.ended():
            self.process_guess(player.get_next_guess())

    def won(self):
        return self.current_guess == self._word

    def lost(self):
        return len(self.guessed_words) >= MAX_WORD_GUESSES

    def ended(self):
        return self.won() or self.lost()

    def to_s(self):
        return "Word: '{}' | Score: {}".format("".join(self.current_guess), self.score)

class Player(object):
    def __init__(self):
        self.possible_guesses = list('eariotnslcudpmhgbfywkvxzjq')

    def get_next_guess(self):
        return self.possible_guesses.pop(0)

if __name__ == '__main__':
    for _ in range(10):
        game = Game()
        player = Player()
        game.play(player)
        print game.to_s()
