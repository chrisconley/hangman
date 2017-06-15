from bitarray import bitarray


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