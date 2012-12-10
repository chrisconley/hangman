#from hangman.game import Game


#rules = {'letter_miss': 1, 'letter_hit': 0, 'word_miss': 1, 'max_word_guesses': 5, 'max_word_guess_score': 25}
#g = Game('hello', rules)

#g.process_letter_guess('a')

#print g.to_s()

#g.process_letter_guess('e')

#print g.to_s()

#g.process_letter_guess('x')
#print g.to_s()

#g.process_word_guess('happy')
#print g.to_s()

#g.process_letter_guess('o')
#print g.to_s()

#import string
#class Game:
    #def __init__(self, word, rules):
        #"""docstring for __init__"""
        #self.word = word
        #self.rules = rules
        #self.current_guess = ['-' for letter in word]
        #self.missed_letters = []
        #self.guessed_words = []

    #def to_s(self):
        #"""docstring for to_s"""
        #template = string.Template("${current_guess} | ${missed_letters} | ${guessed_words}")
        #return template.substitute(self.__dict__)


#def new_game(word, rules):
    #"""docstring for new_game"""
    #return Game(word, rules)

#def calculate_score(game):
    #"""docstring for calcluate_score"""
    #return (len(game.missed_letters) * game.rules['letter_miss']) + (len(game.guessed_words) * game.rules['word_miss'])

#def process_letter_guess(game, guess):
    #"""docstring for process_letter_guess"""
    #for index, letter in enumerate(game.word):
        #if guess == letter: game.current_guess[index] = guess

    #if not guess in game.word:
        #game.missed_letters.append(guess)

#rules = {'letter_miss': 1, 'letter_hit': 0, 'word_miss': 1, 'max_word_guesses': 5, 'max_word_guess_score': 25}
#g = new_game('hello', rules)

#process_letter_guess(g, 'h')
#process_letter_guess(g, 'x')
#process_letter_guess(g, 'o')
#process_letter_guess(g, 'n')
#print g.to_s()
#print calculate_score(g)

class check:
    def __init__(self, word, guesses):
        """docstring for __init__"""
        self.__word = word
        self.__guesses = guesses

    def words(self):
        """docstring for words"""
        return {guess for guess in self.__guesses if len(guess) == len(self.__word)}

    def missed_words(self):
        """docstring for missed_words"""
        return {guess for guess in self.words() if guess != self.__word}

    def letters(self):
        """docstring for letters"""
        return self.__guesses - self.words()

    def known_letters(self):
        """docstring for known_letters"""
        return {letter for letter in self.letters() if letter in self.__word}

    def missed_letters(self):
        """docstring for missed_letters"""
        return self.letters() - self.known_letters()

    def match(self):
        """docstring for match"""
        result = []
        for index, letter in enumerate(self.__word):
            result.append(letter if letter in self.known_letters() else '-')
        return ''.join(result)

    def guesses(self):
        """docstring for word"""
        return self.__guesses

def play(strategy, scorer, word, guesses=set()):
    """docstring for play"""
    result = check(word, guesses)
    if result.match() == word:
        return [word, guesses, scorer(result)]
    else:
        new_guesses = strategy(result)
        return play(strategy, scorer, word, new_guesses)

def score(result):
    """docstring for score"""
    if len(result.missed_words()) >= 5:
        return 25
    else:
        return (len(result.missed_letters()) * 1) + (len(result.missed_words()) * 1)

def naive(previous_result):
    """docstring for next_guess"""
    possible_guesses = 'eariotnslcudpmhgbfywkvxzjq'
    for letter in possible_guesses:
        if letter not in previous_result.guesses():
            return previous_result.guesses() | set(letter)

import random
words = ['cat', 'eat', 'cash', 'bet', 'ear', 'teach']
print play(naive, score, random.choice(words))
