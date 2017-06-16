from collections import defaultdict

from bitarray import bitarray

from games.player_utils import OrderedCounter


class Dictionary(list):
    def words_to_bits(self, words):
        assert type(words) == set, "Words collection must be a set"
        bits = self._initialize_bits()
        for index, code_word in enumerate(self):
            if code_word in words:
                bits[index] = True
        return bits

    def bits_to_words(self, bits):
        assert type(bits) == bitarray, "Bits must be a bitarray"
        return {self[index] for index, bit in enumerate(bits) if bit}

    def _initialize_bits(self):
        bits = bitarray(len(self))
        bits[0:] = False
        return bits


class PotentialOutcomes(dict):
    def __init__(self, data={}):
        self._code_words = set()
        super().__init__(self)
        for guess, responses in data.items():
            for response, code_words in responses.items():
                [self.add(guess, response, w) for w in code_words]

    def add(self, guess, response, code_word):
        if self.get(guess) is None:
            self[guess] = PossibleResponses(guess)
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
    def all_code_words(self):
        return self._code_words


class PossibleResponses(defaultdict):
    def __init__(self, guess):
        self.guess = guess
        super().__init__(set)

    def as_counts(self):
        counter = OrderedCounter()
        for response, code_words in self.items():
            counter[response] = len(code_words)
        return counter

    @classmethod
    def from_dict(cls, guess, data):
        possible_responses = cls(guess)
        for response, code_words in data.items():
            possible_responses[response] = code_words
        return possible_responses