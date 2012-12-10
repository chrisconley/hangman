import hangman.game as hangman
import random
words = ['cat', 'eat', 'cash', 'bet', 'ear', 'teach']
print hangman.play(random.choice(words), hangman.naive_strategy, hangman.default_scorer)

import csv
with open('words.txt', 'rb') as csvfile:
    words = csv.reader(csvfile)
    for word in words:
        print word
