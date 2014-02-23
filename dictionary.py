from collections import defaultdict

from bitarray import bitarray

class EncodedDictionary(dict):
    def __init__(self, words, *args, **kwargs):
        self.words = words
        self.length = len(words)
        self.key_sets = defaultdict(set)
        super(dict, self).__init__()

    def key_set_add(self, key):
        # keys should only ever have one letter in them
        letter = key.replace('-', '')[0]
        self.key_sets[letter].add(key)

    def get_keys(self, letter):
        return self.key_sets[letter]

def initialize_bits(length, initializer=False):
    array = bitarray(length)
    array[0:] = initializer
    return array

def set_default_bits(encoded_dictionary, key):
    bits = encoded_dictionary.get(key)
    if bits is None:
        bits = initialize_bits(encoded_dictionary.length)
        encoded_dictionary[key] = bits
        encoded_dictionary.key_set_add(key)
    return bits

