from collections import Counter
import unittest

def countit(counter, words):
    for word in words:
        word_length = len(word)
        for i, letter in enumerate(word):
            if i == word_length - 1:
                continue
            next_letter = word[i+1]
            key = "{}{}{}".format(letter, next_letter, i)
            counter[key] += 1
    return counter


class BitCounter(unittest.TestCase):

    def test_countit(self):
        counter = Counter()
        words = ['cat', 'cot', 'can']
        counts = countit(counter, words)
        expected_counts = {
            'ca0': 2,
            'co0': 1,
            'at1': 1,
            'ot1': 1,
            'an1': 1
        }
        self.assertEqual(counts, expected_counts)

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentTypeError
    import fileinput

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    args = parser.parse_args()

    counter = Counter()
    words = [word.strip() for word in fileinput.input(args.file)]
    print len(words)
    countit(counter, words)

    print counter
    print len(counter.keys())
