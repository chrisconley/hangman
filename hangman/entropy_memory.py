from __future__ import print_function
from collections import Counter
import math
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
            if letter == 'total':
                continue

            if letter == "$":
                guess_sum = 0
            else:
                guess_sum = 0
                count_key = "".join(sorted("".join([guesses, letter])))
                total_words = float(count_memory[guesses]['total'])
                for next_letter in ALPHABET:
                    if count_memory[count_key][next_letter]:
                        plausibility = count_memory[count_key][next_letter] / total_words
                        guess_sum += -(plausibility * math.log(plausibility))

                # Miss
                total = float(count_memory[count_key]['total'])
                miss_count = (total_words - total)
                if miss_count:
                    plausibility = miss_count / total_words
                    guess_sum += -(plausibility * math.log(plausibility))

            sum_memory.setdefault(guesses, {})
            sum_memory[guesses][letter] = guess_sum

    return sum_memory

class SumMemoryTests(unittest.TestCase):

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
        self.assertAlmostEqual(sum_memory['']['e'], 1.1, places=1)
        self.assertAlmostEqual(sum_memory['']['h'], 1.4, places=1)
        self.assertAlmostEqual(sum_memory['']['s'], 1.7, places=1)

if __name__ == '__main__':
    import csv
    import sys
    print("loading", end='\n', file=sys.stderr)
    memory = load_count_memory(csv.reader(sys.stdin))
    print("generating", end='\n', file=sys.stderr)
    sum_memory = generate_sum_memory(memory)

    print("writing", end='\n', file=sys.stderr)
    writer = csv.writer(sys.stdout)
    for guesses, counts in sum_memory.items():
        for letter, count in counts.items():
            key = ":".join([guesses, letter])
            writer.writerow([key, count])

    unittest.main()

