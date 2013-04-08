class MysteryString(str):
    def __new__(cls, word, guesses):
        result = []
        for index, letter in enumerate(word):
            result.append(letter if letter in guesses else '-')
        match = ''.join(result)
        obj = str.__new__(cls, match)
        obj.word = word
        obj.guesses = guesses
        return obj

    @property
    def words(self):
        return {guess for guess in self.guesses if len(guess) == len(self.word)}

    @property
    def missed_words(self):
        return {guess for guess in self.words if guess != self.word}

    @property
    def letters(self):
        return self.guesses - self.words

    @property
    def known_letters(self):
        return {letter for letter in self.letters if letter in self.word}

    @property
    def missed_letters(self):
        return self.letters - self.known_letters

    @property
    def match(self):
        return self

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

def play(word, strategy=naive_strategy, scorer=default_scorer, guesses=set()):
    result = MysteryString(word, guesses)
    if result == word:
        return [word, guesses, scorer(result)]
    else:
        new_guesses = strategy(result)
        return play(word, strategy, scorer, new_guesses)

if __name__ == '__main__':
    import random
    words = ['cat', 'eat', 'cash', 'bet', 'ear', 'teach']
    print play(random.choice(words))
