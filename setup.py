from hangman.game import Game


rules = {'letter_miss': 1, 'letter_hit': 0, 'word_miss': 1, 'max_word_guesses': 5, 'max_word_guess_score': 25}
g = Game('hello', rules)

g.process_letter_guess('a')

print g.to_s()

g.process_letter_guess('e')

print g.to_s()

g.process_letter_guess('x')
print g.to_s()

g.process_word_guess('happy')
print g.to_s()

g.process_letter_guess('o')
print g.to_s()
