from collections import defaultdict


def get_next_guess_naive(potentials, game_log):
    # If we've whittled down to return one remaining word,
    # return that word as our next guess to finish the game.
    if potentials.total_length == 1:
        return list(potentials.code_words)[0]

    potential_guesses = 'esiarntolcdupmghbyfvkwzxqj'
    worthwhile_guesses = set(''.join(potentials.code_words))
    for guess in potential_guesses:
        if guess in game_log.guesses or guess not in worthwhile_guesses:
            continue
        return guess


class Potential(dict):
    def __init__(self, data={}):
        self._code_words = set()
        super().__init__(self)
        for guess, responses in data.items():
            for response, code_words in responses.items():
                [self.add(guess, response, w) for w in code_words]

    def add(self, guess, response, code_word):
        if self.get(guess) is None:
            self[guess] = defaultdict(set)
        self[guess][response].add(code_word)
        self._code_words.add(code_word)

    def get_by_guess_response(self, guess, response):
        return self[guess][response]

    @property
    def guesses(self):
        return set(self.keys())

    @property
    def total_length(self):
        return len(self._code_words)

    @property
    def code_words(self):
        return self._code_words


def get_potentials(remaining_code_words, get_response, game_log):
    indexed_potentials = Potential()
    potential_guesses = 'esiarntolcdupmghbyfvkwzxqj'
    worthwhile_guesses = set(''.join(remaining_code_words))
    for guess in potential_guesses:
        if guess not in worthwhile_guesses:
            continue
        for code_word in remaining_code_words:
            response = get_response(code_word, guess)
            indexed_potentials.add(guess, response, code_word)
    return indexed_potentials
