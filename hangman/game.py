from hangman.mystery_string import subclazz as mystery_string

def default_scorer(result):
    """docstring for score"""
    if len(result.missed_words()) >= 5:
        return 25
    else:
        return (len(result.missed_letters()) * 1) + (len(result.missed_words()) * 1)

def naive_strategy(previous_result):
    """docstring for next_guess"""
    possible_guesses = 'eariotnslcudpmhgbfywkvxzjq'
    for letter in possible_guesses:
        if letter not in previous_result.guesses():
            return previous_result.guesses() | set(letter)

def play(word, strategy=naive_strategy, scorer=default_scorer, guesses=set()):
    """docstring for play"""
    result = mystery_string(word, guesses)
    if result == word:
        return [word, guesses, scorer(result)]
    else:
        new_guesses = strategy(result)
        return play(word, strategy, scorer, new_guesses)

