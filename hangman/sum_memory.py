from collections import Counter
import unittest

from hangman.strat import learn_word

ALPHABET = 'abcdefghijklmnopqrstuvwxyz$'


def make_key(guesses, next_letter):
    guesses = set(''.join(guesses))
    return ":".join([''.join(sorted(guesses)), next_letter])

def load_count_memory(reader):
    memory = {}
    for row in reader:
        key = row[0]
        count = int(row[1])
        guesses, letter = key.split(':')

        counter = memory.setdefault(guesses, Counter())
        counter[letter] = count

    return memory



def generate_sum_memory(count_memory):
    sum_memory = {}
    for guesses, counter in count_memory.items():

        for letter, count in counter.items():

            if letter == "$":
                guess_sum = count
            else:
                guess_sum = 0
                count_key = "".join(sorted("".join([guesses, letter])))
                for next_letter in ALPHABET:
                    guess_sum += count_memory[count_key][next_letter]

            sum_memory.setdefault(guesses, {})
            sum_memory[guesses][letter] = guess_sum

    return sum_memory

class SumMemoryTests(unittest.TestCase):
    #maxDiff = None

    def test_load_and_generate(self):
        words = ['synth', 'sites', 'siete']
        counter = {}
        for word in words:
            counter = learn_word(word, counter)

        reader = []
        for key, count in counter.items():
            row = [key, count]
            reader.append(row)

        count_memory = load_count_memory(reader)
        sum_memory = generate_sum_memory(count_memory)

        """
        This is saying if my current guesses are "es", then there are two words with an "i" in them and two words
        with a "t" in them.

        The sum_memory can then say, if my guesses are currently "e", the sum of the total words available is 4 if
        I guess "s" on my next guess.
        """
        self.assertEqual(count_memory[''], Counter({'s': 3, 't': 3, 'e': 2, 'i': 2, 'h': 1, 'n': 1, 'y': 1}))
        self.assertEqual(count_memory['t'], Counter({'s': 3, 'e': 2, 'i': 2, 'h': 1, 'n': 1, 'y': 1}))
        self.assertEqual(count_memory['e'], Counter({'s': 2, 'i': 2, 't': 2}))

        self.assertEqual(count_memory['es'], Counter({'i': 2, 't': 2}))
        self.assertEqual(sum_memory[''], {'e': 6, 'i': 6, 'h': 4, 'n': 4, 's': 10, 't': 10, 'y': 4})
        self.assertEqual(sum_memory['e'], {'s': 4, 'i': 4, 't': 4})
        self.assertEqual(sum_memory['t'], {'e': 4, 'i': 4, 'h': 3, 'n': 3, 's': 7, 'y': 3})
        self.assertEqual(sum_memory['es'], {'i': 2, 't': 2})
        self.assertEqual(sum_memory['eis'], {'t': 2})
        self.assertEqual(sum_memory['est'], {'i': 2})
        self.assertEqual(sum_memory['eist'], {'$': 2})

        self.assertEqual(count_memory['hnsy'], Counter({'t': 1}))

        self.assertEqual(count_memory['hnsty'], Counter({'$': 1}))

if __name__ == '__main__':
    #import csv
    #import sys #memory = load_count_memory(csv.reader(sys.stdin))

    #sum_memory = generate_sum_memory(memory)

    #print sum_memory

    #assert memory == sum_memory
    unittest.main()
