from hangman.game import Game


rules = {'letter_miss': 1, 'letter_hit': 0, 'word_miss': 1, 'max_word_guesses': 5, 'max_word_guess_score': 25}
g = Game('hello', rules)
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
