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

def extract(word, guesses):
    """docstring for extract"""
    words = {guess for guess in guesses if len(guess) == len(word)}
    missed_words = {guess for guess in words if guess != word}
    letters = guesses - words
    known_letters = {letter for letter in letters if letter in word}
    missed_letters = letters - known_letters
    match = (len(words - missed_words) == 1) | (known_letters == set(word))
    return [missed_letters, known_letters, missed_words, match]

def score(word, guesses):
    """docstring for score"""
    missed_letters, known_letters, missed_words, _ = extract(word, guesses)
    if len(missed_words) >= 5:
        return 25
    else:
        return (len(missed_letters) * 1) + (len(missed_words) * 1)

def check(word, guesses):
    """docstring for guess"""
    missed_letters, known_letters, _, match = extract(word, guesses)
    if match:
        return word
    else:
        result = []
        for index, letter in enumerate(word):
            result.append(letter if letter in known_letters else '-')
        return ''.join(result)

def play(strategy, word, guesses=set()):
    """docstring for play"""
    _,_,_, match = extract(word, guesses)
    if match:
        return [word, guesses, score(word, guesses)]
    else:
        return play(strategy, word, strategy(check(word, guesses), guesses))

def strategy(current, previous_guesses):
    """docstring for next_guess"""
    possible_guesses = 'eariotnslcudpmhgbfywkvxzjq'
    for letter in possible_guesses:
        if letter not in previous_guesses:
            return previous_guesses | set(letter)

import random
words = ['cat', 'eat', 'cash', 'bet', 'ear', 'teach']
print play(strategy, random.choice(words))
