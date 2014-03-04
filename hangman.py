from mystery_string import MysteryString

def play(word):
    result = MysteryString(word, set())
    while True:
        if result == word:
            break
        next_guess = (yield result)
        if next_guess:
            new_guesses = result.guesses | set(next_guess)
            result = MysteryString(word, new_guesses)
