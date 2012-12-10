from hangman.mystery_string import subclazz as check

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
#print check('cat', {'cat', 'bet'})
