class MysteryString(str):
    def __new__(cls, word, guesses, delimiter='-'):
        result = [
            (letter if letter in guesses else delimiter)
            for index, letter
            in enumerate(word)]
        match = ''.join(result)
        obj = str.__new__(cls, match)
        obj.word = word
        obj.guesses = guesses
        return obj

    @property
    def guessed_words(self):
        return {guess for guess in self.guesses if len(guess) == len(self.word)}

    @property
    def missed_words(self):
        return {guess for guess in self.guessed_words if guess != self.word}

    @property
    def guessed_letters(self):
        return self.guesses - self.guessed_words

    @property
    def known_letters(self):
        return {letter for letter in self.guessed_letters if letter in self.word}

    @property
    def missed_letters(self):
        return self.guessed_letters - self.known_letters

def default_scorer(result):
    if len(result.missed_words) >= 5:
        return 25
    else:
        return (len(result.missed_letters) * 1) + (len(result.missed_words) * 1)

def naive_strategy(previous_result):
    possible_guesses = 'eariotnslcudpmhgbfywkvxzjq'
    for letter in possible_guesses:
        if letter not in previous_result.guesses:
            return previous_result.guesses | set(letter)

def play(word):
    result = MysteryString(word, set())
    while result != word:
        next_guess = (yield result)
        if next_guess:
            new_guesses = result.guesses | set(next_guess)
            result = MysteryString(word, new_guesses)


if __name__ == '__main__':
    import random
    words = ['cat', 'eat', 'cash', 'bet', 'ear', 'teach']
    print play(random.choice(words))
