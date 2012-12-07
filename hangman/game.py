import string
class Game:

    def __init__(self, word, rules):
        """docstring for __init__"""
        self.word = list(word)
        self.rules = rules
        self.current_guess = ['-' for letter in word]
        self.score = 0
        self.known_letters = []
        self.missed_letters = []
        self.guessed_words = []
        self.ended = False

    def process_letter_guess(self, guess):
        """docstring for process_letter_guess"""
        if guess in self.word:
            self.known_letters.append(guess)
            self.current_guess = [(guess if guess == word_letter else '-') for word_letter in self.word]
            self.score += self.rules['letter_hit']
        else:
            self.missed_letters.append(guess)
            self.score += self.rules['letter_miss']

    def process_word_guess(self, guess):
        """docstring for process_word_guess"""
        self.guessed_words.append(guess)
        if guess == self.word:
            self.current_guess = self.word
            self.ended = True
        elif len(self.guessed_words) >= self.rules['max_word_guesses']:
            self.score = self.rules['max_word_guess_score']
            self.ended = True
        else:
            self.score += self.rules['word_miss']

    def won(self):
        self.current_guess == self.word

    def lost(self):
        self.ended and not(self.won)

    def to_s(self):
        """docstring for to_s"""
        template = string.Template("${current_guess} | ${missed_letters} | ${guessed_words} | ${score}")
        return template.substitute(self.__dict__)
