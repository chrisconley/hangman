from collections import Counter
import unittest
from bitstring import BitArray

def get_key(letter, next_letter, i):
    key = "{}{}{}".format(letter, next_letter, i)
    return key


def countit(counter, words):
    dictionary_length = len(words)
    for word_index, word in enumerate(words):
        word_length = len(word)
        for i, letter in enumerate(word):
            if i == word_length - 1:
                continue
            next_letter = word[i+1]
            key = get_key(letter, next_letter, i)
            bitarray = counter.setdefault(key, BitArray(dictionary_length))
            bitarray.set(1, word_index)
    return counter

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def search(dictionary_length, graph, mystery_string):
    union = BitArray(dictionary_length)
    #union.invert([0, -1])
    word_length = len(mystery_string)
    for i, letter in enumerate(mystery_string):
        print i, letter
        if i == word_length - 1:
            continue
        next_letter = mystery_string[i+1]
        if letter == '-' and next_letter == '-':
            for first_letter in ALPHABET:
                for second_letter in ALPHABET:
                    key = get_key(first_letter, second_letter, i)
                    bitarray = graph.get(key, None)
                    if bitarray:
                        print union, bitarray
                        union = union | bitarray
        elif letter == '-' and next_letter != '-':
            for first_letter in ALPHABET:
                    key = get_key(first_letter, next_letter, i)
                    bitarray = graph.get(key, None)
                    if bitarray:
                        print union, bitarray
                        union = union | bitarray
        elif letter != '-' and next_letter == '-':
            for second_letter in ALPHABET:
                    key = get_key(letter, second_letter, i)
                    bitarray = graph.get(key, None)
                    if bitarray:
                        print union, bitarray
                        union = union | bitarray

        else:
            key = get_key(letter, next_letter, i)
            bitarray = graph[key]
            print union, bitarray
            union = union | bitarray
    count = len([x for x in BitArray(union) if x])
    return count



class BitCounter(unittest.TestCase):

    def test_countit(self):
        counter = {}
        words = ['cat', 'cot', 'can']
        counts = countit(counter, words)
        expected_counts = {
            'ca0': BitArray('0b101'),
            'co0': BitArray('0b010'),
            'at1': BitArray('0b100'),
            'ot1': BitArray('0b010'),
            'an1': BitArray('0b001')
        }
        self.assertEqual(counts, expected_counts)

    def test_search(self):
        graph = {}
        words = ['cat', 'cot', 'can']
        countit(graph, words)
        #self.assertEqual(search(len(words), graph, '-at'), 1)
        #self.assertEqual(search(len(words), graph, '---'), 3)
        #self.assertEqual(search(len(words), graph, '-a-'), 2)
        #self.assertEqual(search(len(words), graph, 'ca-'), 2)
        self.assertEqual(search(len(words), graph, 'can'), 1)

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import fileinput

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    args = parser.parse_args()

    counter = {}
    words = [word.strip() for word in fileinput.input(args.file)]
    print len(words)
    countit(counter, words)

    for key, a in counter.items():
        print key, a
    print len(counter.keys())

    import time
    time.sleep(30)
