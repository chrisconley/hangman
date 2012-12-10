import hangman.game as hangman
import random
words = ['cat', 'eat', 'cash', 'bet', 'ear', 'teach']
print hangman.play(random.choice(words), hangman.naive_strategy, hangman.default_scorer)

import csv
import pydawg
words = []
dawg = pydawg.DAWG()

with open('words-short.txt', 'rb') as csvfile:
    wordfile = csv.reader(csvfile)
    for row in wordfile:
        if row:
            dawg.add_word(row[0])
            #words.append(row[0])

#words.sort()
#print words
#for word in words:
    #print word
    #dawg.add_word(word)
print '@@@'
#print random.choice(words)

print dawg.word2index('abet')
print dawg.index2word(161)
print dawg.index2word(20)
print dawg.search('abet')
