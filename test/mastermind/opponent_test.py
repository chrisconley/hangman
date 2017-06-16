import unittest

from games.mastermind import opponent, word_generator


class MastermindOpponentTests(unittest.TestCase):
    def test_get_unique_guesses_full_mastermind(self):
        words = word_generator.generate_words('ABCDEF', 4)
        self.assertEqual(opponent.get_unique_guesses(words), [
            'AAAA',
            'AAAB',
            'AABB',
            'AABC',
            'ABCD'
        ])

    def test_get_unique_guesses_short_symbols(self):
        words = word_generator.generate_words('ABC', 4)
        self.assertEqual(opponent.get_unique_guesses(words), [
            'AAAA',
            'AAAB',
            'AABB',
            'AABC',
        ])

    def test_get_unique_guesses_truncated_word_list(self):
        words = ['BBBB', 'AAAB', 'AABC']
        self.assertEqual(opponent.get_unique_guesses(words), [
            'AAAB',
            'AABC',
            'BBBB'
        ])

    def test_get_integer_partitions(self):
        # https://en.wikipedia.org/wiki/Partition_(number_theory)
        # http://stackoverflow.com/a/10036764/67184

        partitions = opponent.get_integer_partitions(4)
        self.assertEqual(partitions, {
            (4,),
            (3, 1),
            (2, 2),
            (2, 1, 1),
            (1, 1, 1, 1),
        })

        partitions = opponent.get_integer_partitions(5)
        self.assertEqual(partitions, {
            (5,),
            (4, 1),
            (3, 2),
            (3, 1, 1),
            (2, 2, 1),
            (2, 1, 1, 1),
            (1, 1, 1, 1, 1),
        })

    def test_partition_word(self):
        partition = opponent.partition_word('AAAA')
        self.assertEqual(partition, (4,))
        partition = opponent.partition_word('BBBB')
        self.assertEqual(partition, (4,))
        partition = opponent.partition_word('AABB')
        self.assertEqual(partition, (2, 2))
        partition = opponent.partition_word('AAAB')
        self.assertEqual(partition, (3, 1))
        partition = opponent.partition_word('ABBB')
        self.assertEqual(partition, (3, 1))
        partition = opponent.partition_word('ABCD')
        self.assertEqual(partition, (1, 1, 1, 1))

    def test_get_potential_next_guesses(self):
        words = ['YYY', 'YYR', 'YRY', 'RYY', 'YRR', 'RYR', 'RRY', 'RRR']
        potentials = opponent.get_potentials(words, opponent.get_response, opponent.GameLog())
        self.assertEqual(potentials, {
            'RRR': {
                'BBB': {'RRR'}, 'BB': {'RRY', 'YRR', 'RYR'}, 'B': {'RYY', 'YYR', 'YRY'}, '': {'YYY'}
            },
            'RRY': {
                'BB': {'RRR', 'RYY', 'YRY'}, 'BWW': {'YRR', 'RYR'}, 'BBB': {'RRY'}, 'WWW': {'YYR'}, 'B': {'YYY'}
            }
        })
