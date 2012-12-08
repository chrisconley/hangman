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

def score(word, guesses):
    """docstring for score"""
    pass

def guess(current, word, guesses):
    """docstring for guess"""
    words = [guess for guess in guesses if len(guess) == word]
    letters = [guess for guess in guesses if len(guess) != word]
    new = list(current)
    if word in guesses:
        return [word, guesses]
    else:
        for guess in letters:
            for index, letter in enumerate(word):
                if guess == letter: new[index] = guess
        return (''.join(new), guesses)

print guess("---", "cat", ["a"])
print guess("-a-", "cat", ["a", 'x'])
print guess("-a-", "cat", ["a", 'x', 't'])
print guess("-at", "cat", ["a", 'x', 't', 'bat'])
print guess("-at", "cat", ["a", 'x', 't', 'bat', 'cat'])
