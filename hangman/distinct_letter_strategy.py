from collections import Counter
import csv

import hangman.game as game

MEMORY = {}
# we need to pass this in as an argument
with open('hangman/entropy_counts.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        key, letter = row[0].split(':')
        count = float(row[1])
        counter = MEMORY.setdefault(key, Counter())
        counter[letter] = count

FIRST_GUESSES = 'eariotnslcudpmhgbfywkvxzjq'


def f1(d1, ignore_keys):
     v=list(d1.values())
     k=list(set(d1.keys()) - ignore_keys)
     return k[v.index(max(v))]

def strategy(previous_result):
    if not previous_result.known_letters:
        for letter in FIRST_GUESSES:
            if letter not in previous_result.guesses:
                return previous_result.guesses | set(letter)

    key = ''.join(sorted(previous_result.known_letters))
    counter = MEMORY[key]
    #print previous_result
    #print counter
    for letter, count in counter.most_common():
        if letter not in previous_result.guesses:
            #print previous_result.guesses
            #print letter
            return previous_result.guesses | set(letter)
    #print 'hi'

if __name__ == '__main__':
    import csv
    import fileinput
    import sys
    total = 0
    for word in fileinput.input():
        result = game.play(word.strip(), strategy=strategy)
        total += result[2]
    print total
