import unittest

from games.mastermind import player, opponent


class MastermindPlayerTests(unittest.TestCase):
    def test_count_mastermind_brute_responses_two_letter_two_colors(self):
        words = ['YY', 'YR', 'RY', 'RR']
        counter = player.count_mastermind_letters_brute(words, opponent.get_response)
        self.assertEqual(counter['*'], 4)
        self.assertListEqual(sorted(list(counter.keys())), sorted(['*', 'YY', 'YR', 'RY', 'RR']))
        self.assertEqual(counter['YY'], {'*': 4, '': 1, 'B': 2, 'BB': 1})
        self.assertEqual(counter['YR'], {'*': 4, 'B': 2, 'WW': 1, 'BB': 1})
        self.assertEqual(counter['RY'], {'*': 4, 'B': 2, 'WW': 1, 'BB': 1})
        self.assertEqual(counter['RR'], {'*': 4, '': 1, 'B': 2, 'BB': 1})

    def test_count_mastermind_brute_responses_two_letter_three_colors(self):
        words = ['YY', 'RR', 'CC', 'YR', 'RY', 'YC', 'CY', 'CR', 'RC']
        counter = player.count_mastermind_letters_brute(words, opponent.get_response)
        self.assertEqual(counter['*'], 9)
        self.assertEqual(counter['YY'], {'*': 9, '': 4, 'B': 4, 'BB': 1})
        self.assertEqual(counter['RR'], {'*': 9, '': 4, 'B': 4, 'BB': 1})
        self.assertEqual(counter['CC'], {'*': 9, '': 4, 'B': 4, 'BB': 1})
        self.assertEqual(counter['YR'], {'*': 9, '': 1, 'B': 4, 'W': 2, 'WW': 1, 'BB': 1})
        self.assertEqual(counter['RY'], {'*': 9, '': 1, 'B': 4, 'W': 2, 'WW': 1, 'BB': 1})
        self.assertEqual(counter['YC'], {'*': 9, '': 1, 'B': 4, 'W': 2, 'WW': 1, 'BB': 1})
        self.assertEqual(counter['CY'], {'*': 9, '': 1, 'B': 4, 'W': 2, 'WW': 1, 'BB': 1})
        self.assertEqual(counter['CR'], {'*': 9, '': 1, 'B': 4, 'W': 2, 'WW': 1, 'BB': 1})
        self.assertEqual(counter['RC'], {'*': 9, '': 1, 'B': 4, 'W': 2, 'WW': 1, 'BB': 1})

    def test_count_mastermind_brute_responses_three_letter_two_colors(self):
        words = ['YYY', 'YYR', 'YRY', 'RYY', 'YRR', 'RYR', 'RRY', 'RRR']
        assert sorted(words) == opponent.generate_words('YR', 3)
        counter = player.count_mastermind_letters_brute(words, opponent.get_response)
        self.assertEqual(counter['*'], 8)
        self.assertEqual(counter['YYY'], {'*': 8, 'BBB': 1, 'BB': 3, 'B': 3, '': 1})
        self.assertEqual(counter['YYR'], {'*': 8, 'BB': 3, 'BWW': 2, 'BBB': 1, 'WWW': 1, 'B': 1})
        self.assertEqual(counter['YRY'], {'*': 8, 'BB': 3, 'BWW': 2, 'BBB': 1, 'WWW': 1, 'B': 1})
        self.assertEqual(counter['RYY'], {'*': 8, 'BB': 3, 'BWW': 2, 'BBB': 1, 'WWW': 1, 'B': 1})
        self.assertEqual(counter['YRR'], {'*': 8, 'BB': 3, 'BWW': 2, 'BBB': 1, 'WWW': 1, 'B': 1})
        self.assertEqual(counter['RYR'], {'*': 8, 'BB': 3, 'BWW': 2, 'BBB': 1, 'WWW': 1, 'B': 1})
        self.assertEqual(counter['RRY'], {'*': 8, 'BB': 3, 'BWW': 2, 'BBB': 1, 'WWW': 1, 'B': 1})
        self.assertEqual(counter['RRR'], {'*': 8, 'BBB': 1, 'BB': 3, 'B': 3, '': 1})

    def test_count_mastermind_brute_real_mastermind(self):
        words = opponent.generate_words('ABCDEF', 4)
        self.assertEqual(len(words), 1296)

        counter = player.count_mastermind_letters_brute(words, opponent.get_response)

        self.assertEqual(counter['AAAA'], {'*': 1296, '': 625, 'B': 500, 'BB': 150, 'BBB': 20, 'BBBB': 1})
        self.assertEqual(counter['AAAB'], {'*': 1296, 'B': 317, '': 256, 'W': 244, 'BB': 123, 'BW': 108, 'WWW': 64, 'WWWW': 61, 'BWW': 48, 'BWWW': 27, 'BBW': 24, 'BBB': 20, 'BBWW': 3, 'BBBB': 1})
        self.assertEqual(counter['ABCD'], {'*': 1296, 'WW': 312, 'BW': 252, 'W': 152, 'WWW': 136, 'BWW': 132, 'B': 108, 'BB': 96, 'BBW': 48, 'BBB': 20, '': 16, 'WWWW': 9, 'BWWW': 8, 'BBWW': 6, 'BBBB': 1})
        self.assertEqual(counter['AABB'], {'*': 1296, 'WW': 288, 'B': 256, '': 256, 'BW': 144, 'BB': 114, 'WWWW': 81, 'BWW': 64, 'BWWW': 36, 'BBW': 32, 'BBB': 20, 'BBWW': 4, 'BBBB': 1})
        self.assertEqual(counter['AABC'], {'*': 1296, 'W': 222, 'BW': 198, 'B': 182, 'WW': 160, 'WWW': 130, 'BB': 105, 'BWW': 98, '': 81, 'BBW': 40, 'WWWW': 32, 'BWWW': 22, 'BBB': 20, 'BBWW': 5, 'BBBB': 1})

        self.assertEqual(dict(counter['AAAA']), dict(counter['DDDD']))
        self.assertEqual(dict(counter['AAAB']), dict(counter['DDDE']))
        self.assertEqual(dict(counter['AABB']), dict(counter['DDEE']))
        self.assertEqual(dict(counter['AABC']), dict(counter['DDEF']))
        self.assertEqual(dict(counter['ABCD']), dict(counter['DEFA']))
        self.assertEqual(dict(counter['ABCD']), dict(counter['ABCE']))

    def test_count_mastermind_fast_real_mastermind(self):
        words = opponent.generate_words('ABCDEF', 4)
        self.assertEqual(len(words), 1296)

        brute_counter = player.count_mastermind_letters_brute(words, opponent.get_response)
        fast_counter = player.count_mastermind_letters(words, opponent.get_response)
        self.assertEqual(sorted(fast_counter.keys()), [
            '*',
            'AAAA',
            'AAAB',
            'AABB',
            'AABC',
            'ABCD'
        ])

        self.assertEqual(dict(brute_counter['AAAA']), dict(fast_counter['AAAA']))
        self.assertEqual(dict(brute_counter['AAAB']), dict(fast_counter['AAAB']))
        self.assertEqual(dict(brute_counter['AABB']), dict(fast_counter['AABB']))
        self.assertEqual(dict(brute_counter['AABC']), dict(fast_counter['AABC']))
        self.assertEqual(dict(brute_counter['ABCD']), dict(fast_counter['ABCD']))
