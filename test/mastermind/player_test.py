import unittest

from games.mastermind import player, opponent
from games import code_words


class MastermindPlayerTests(unittest.TestCase):
    def assertDecimalAlmostEqual(self, actual, expected, places):
        self.assertEqual(type(actual), player.Decimal)
        self.assertAlmostEqual(float(actual), float(expected), places=places)

    def test_get_pmf_for_success(self):
        possible_responses = code_words.PossibleResponses.from_dict(guess='blah', data={
            '': {'1234', '4321'},
            'BB': {'3155'},
            'BBBB': {'3136'},
            'BBW': {'3166', '6136'}
        })
        pmf = player._get_pmf_for_success(possible_responses)
        self.assertEqual(sorted(pmf.keys()), ['!', '*'])
        self.assertDecimalAlmostEqual(pmf['*'], player.Decimal('0.4583333333'), places=9)
        self.assertDecimalAlmostEqual(pmf['!'], player.Decimal('0.5416666667'), places=9)
