from hangman_opponent import HangmanGameState

def play(word):
    result = HangmanGameState(word, set())
    while True:
        if result == word:
            break
        next_guess = (yield result)
        if next_guess:
            new_guesses = result.guesses | set(next_guess)
            result = HangmanGameState(word, new_guesses)
