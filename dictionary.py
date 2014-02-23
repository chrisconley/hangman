from bitarray import bitarray

class EncodedDictionary(dict):
    def __init__(self, words, *args, **kwargs):
        self.words = words
        self.length = len(words)
        super(dict, self).__init__()

def initialize_bits(length, initializer=False):
    array = bitarray(length)
    array[0:] = initializer
    return array

def set_default_bits(encoded_dictionary, key):
    bits = encoded_dictionary.get(key)
    if bits is None:
        bits = initialize_bits(encoded_dictionary.length)
        encoded_dictionary[key] = bits
    return bits

