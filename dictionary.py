from collections import defaultdict

from bitarray import bitarray


def get_keys(word):
    for letter in set(word):
        if letter == '-':
            continue
        yield ''.join([l if l == letter else '-' for l in word])


class EncodedDictionary(dict):
    def __init__(self, words):
        self.words = words
        self.length = len(words)
        self.key_sets = defaultdict(set)
        super(dict, self).__init__()

    def set_default_bits(self, key):
        bits = self.get(key)
        if bits is None:
            bits = _initialize_bits(self.length)
            self[key] = bits
            self.add_key_for_letter(key)
        return bits

    def add_key_for_letter(self, key):
        # keys should only ever have one letter in them
        letter = key.replace('-', '')[0]
        self.key_sets[letter].add(key)

    def get_keys_for_letter(self, letter):
        return self.key_sets[letter]


def encode_dictionary(words):
    """
    Args:
        words: List of words

    Example:

    encode_dictionary(['cat', 'cot', 'can'])

    {
        'c--': bitarray('111'),
        '-a-': bitarray('101'),
        '-o-': bitarray('010'),
        '--n': bitarray('001'),
        '--t': bitarray('110'),
    }

    Explanation: The `c--` key matches all three words, which we
    encode as `111`. The `-o-` key only matches the second word,
    which we encode as `010`.

    """
    encoded_dictionary = EncodedDictionary(words)
    for word_index, word in enumerate(words):
        for key in get_keys(word):
            bits = encoded_dictionary.set_default_bits(key)
            bits[word_index] = True
    return encoded_dictionary


def search(encoded_dictionary, game_state, rejected_letters=''):
    """
    This method takes an encoded dictionary, game state and
    rejected letters (missed letters) and returns a bitarray
    that indicates which words in the dictionary still match.
    """

    """
    Here we're going to get the keys from our game state,
    then look those keys up in our encoded dictionary. We
    continually perform logical AND with each key, so that
    we're left with a bitarray that indicates what words match
    ALL of our keys.

    Ex: With words ['cat', 'cot', 'can'] and game_state '-a-',
    we'll end up with bitarray('101') in `bits`.
    """
    bits = _initialize_bits(encoded_dictionary.length, True)
    for key in get_keys(game_state):
        key_bits = encoded_dictionary[key]
        bits &= key_bits

    """
    Now we have to kick out words that have letters that we don't want.
    We do this by going through all keys that contain those letters
    and continually perform a logical OR with the bitarrays for those
    keys. This gives us every word that has one those rejected letters.

    Since we want every word that does NOT have one of those letters,
    we invert the bitarray as the last step.

    Ex: With words ['cat', 'cot', 'can'] and rejected letters ['n'],
    we'll end up bitarray('001') before inversion and bitarray('110')
    after.
    """
    key_bits = _initialize_bits(encoded_dictionary.length, False)
    for letter in rejected_letters:
        for key in encoded_dictionary.get_keys_for_letter(letter):
            letter_bits = encoded_dictionary[key]
            key_bits |= letter_bits
    key_bits.invert()

    """
    Finally, we perform a logical AND on our two bitarrays to
    get a final bitarray that indicates which words still match
    our current game state.
    """
    bits &= key_bits

    return bits


def get_remaining_words(encoded_words, words):
    return [words[index] for (index, bit) in enumerate(encoded_words) if bit]


def filter_words(encoded_dictionary, game_state, rejected_letters=''):
    """
    This method is used to whittle down a dictionary of words into the
    set of words that still match the state of the game.

    This method first performs a search to return the bitarray that
    indicates which words still match the game state. It then turns
    that bitarray into actual words.
    """
    bits = search(encoded_dictionary, game_state, rejected_letters)
    words = get_remaining_words(bits, encoded_dictionary.words)
    return words


def _initialize_bits(length, initializer=False):
    array = bitarray(length)
    array[0:] = initializer
    return array
