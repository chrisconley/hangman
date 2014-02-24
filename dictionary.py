"""
To run doctests:
nosetests --with-doctest dictionary
"""
from collections import defaultdict

from bitarray import bitarray

def distinct_letters(word):
    """
    >>> [key for key in distinct_letters('coto')]
    ['c', 't', 'o']

    >>> [key for key in distinct_letters('-o-o')]
    ['o']

    >>> [key for key in distinct_letters('-oto')]
    ['t', 'o']
    """
    for letter in set(word):
        if letter == '-':
            continue
        yield letter

def duplicate_letters(word):
    """
    >>> [key for key in duplicate_letters('coto')]
    ['c', 't', 'oo']

    >>> [key for key in duplicate_letters('-o-o')]
    ['oo']

    >>> [key for key in duplicate_letters('-oto')]
    ['t', 'oo']
    """
    for letter in set(word):
        if letter == '-':
            continue
        yield ''.join([l for l in word if l == letter])

def positional_letters(word):
    """
    >>> [key for key in positional_letters('coto')]
    ['c---', '--t-', '-o-o']

    >>> [key for key in positional_letters('-o-o')]
    ['-o-o']

    >>> [key for key in positional_letters('-oto')]
    ['--t-', '-o-o']
    """
    for letter in set(word):
        if letter == '-':
            continue
        yield ''.join([l if l == letter else '-' for l in word])

KEY_GENERATORS = {
    'distinct': distinct_letters,
    'duplicate': duplicate_letters,
    'positional': positional_letters
}

class EncodedDictionary(dict):
    def __init__(self, words, key_generator):
        self.words = words
        self.length = len(words)
        self.key_sets = defaultdict(set)
        self.key_generator = KEY_GENERATORS[key_generator]
        super(dict, self).__init__()

    def set_default_bits(self, key):
        bits = self.get(key)
        if bits is None:
            bits = initialize_bits(self.length)
            self[key] = bits
            self.add_key_for_letter(key)
        return bits

    def add_key_for_letter(self, key):
        # keys should only ever have one letter in them
        letter = key.replace('-', '')[0]
        self.key_sets[letter].add(key)

    def get_keys_for_letter(self, letter):
        return self.key_sets[letter]

def encode_dictionary(words, key_generator):
    encoded_dictionary = EncodedDictionary(words, key_generator)
    for word_index, word in enumerate(words):
        for key in encoded_dictionary.key_generator(word):
            bits = encoded_dictionary.set_default_bits(key)
            bits[word_index] = True
    return encoded_dictionary

def search(encoded_dictionary, mystery_string, rejected_letters=''):
    bits = initialize_bits(encoded_dictionary.length, True)
    for key in encoded_dictionary.key_generator(mystery_string):
        key_bits = encoded_dictionary[key]
        bits &= key_bits

    key_bits = initialize_bits(encoded_dictionary.length, False)
    for letter in rejected_letters:
        for key in encoded_dictionary.get_keys_for_letter(letter):
            letter_bits = encoded_dictionary[key]
            key_bits |= letter_bits
    key_bits.invert()
    bits &= key_bits

    return bits

def initialize_bits(length, initializer=False):
    array = bitarray(length)
    array[0:] = initializer
    return array
