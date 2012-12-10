class clazz:
    def __init__(self, word, guesses):
        """docstring for __init__"""
        self.__word = word
        self.__guesses = guesses

    def words(self):
        """docstring for words"""
        return {guess for guess in self.__guesses if len(guess) == len(self.__word)}

    def missed_words(self):
        """docstring for missed_words"""
        return {guess for guess in self.words() if guess != self.__word}

    def letters(self):
        """docstring for letters"""
        return self.__guesses - self.words()

    def known_letters(self):
        """docstring for known_letters"""
        return {letter for letter in self.letters() if letter in self.__word}

    def missed_letters(self):
        """docstring for missed_letters"""
        return self.letters() - self.known_letters()

    def match(self):
        """docstring for match"""
        result = []
        for index, letter in enumerate(self.__word):
            result.append(letter if letter in self.known_letters() else '-')
        return ''.join(result)

    def guesses(self):
        """docstring for word"""
        return self.__guesses

def closure(word, _guesses):
    def guesses():
        """docstring for word"""
        return _guesses

    def words():
        """docstring for words"""
        return {guess for guess in guesses() if len(guess) == len(word)}

    def missed_words():
        """docstring for missed_words"""
        return {guess for guess in words() if guess != word}

    def letters():
        """docstring for letters"""
        return guesses() - words()

    def known_letters():
        """docstring for known_letters"""
        return {letter for letter in letters() if letter in word}

    def missed_letters():
        """docstring for missed_letters"""
        return letters() - known_letters()

    def match():
        """docstring for match"""
        result = []
        for index, letter in enumerate(word):
            result.append(letter if letter in known_letters() else '-')
        return ''.join(result)


    return dash({
        'guesses': guesses,
        'words': words,
        'missed_words': missed_words,
        'letters': letters,
        'known_letters': known_letters,
        'missed_letters': missed_letters,
        'match': match,
    })

class dash(dict):
    def __getattr__(self, method_name):
        """
            This is called every time a class method or property
            is checked and/or called.

            In here we'll return a new function to handle what we
            want to do.
        """

        if method_name in self:
            return self[method_name]
        else:
            # If the method isn't in our dictionary, act normal.
            raise AttributeError, method_name

class subclazz(str):
    def __new__(clazz, word, guesses):
        """docstring for __init__"""
        result = []
        for index, letter in enumerate(word):
            result.append(letter if letter in guesses else '-')
        match = ''.join(result)
        obj = str.__new__(clazz, match)
        obj.__word = word
        obj.__guesses = guesses
        return obj

    def words(self):
        """docstring for words"""
        return {guess for guess in self.__guesses if len(guess) == len(self.__word)}

    def missed_words(self):
        """docstring for missed_words"""
        return {guess for guess in self.words() if guess != self.__word}

    def letters(self):
        """docstring for letters"""
        return self.__guesses - self.words()

    def known_letters(self):
        """docstring for known_letters"""
        return {letter for letter in self.letters() if letter in self.__word}

    def missed_letters(self):
        """docstring for missed_letters"""
        return self.letters() - self.known_letters()

    def guesses(self):
        """docstring for word"""
        return self.__guesses

    def match(self):
        """docstring for match"""
        return self
