import unittest

from games import play, code_words
from games.mastermind import player, opponent


class MastermindPlayTests(unittest.TestCase):

    def test_play(self):
        words = code_words.Dictionary(['YYY', 'YYR', 'YRY', 'RYY', 'YRR', 'RYR', 'RRY', 'RRR'])
        word, game_log = play.play(
            'YRY',
            words,
            opponent.get_potentials,
            player.build_strategy(info_focus=1.0, success_focus=0.0),
            opponent.get_response,
            opponent.GameLog(),
            use_cache=False,
        )

        self.assertEqual(word, 'YRY')
        self.assertEqual(game_log, [
            {'guess': 'RRY', 'result': 'BB'},
            {'guess': 'RYY', 'result': 'BWW'},
            {'guess': 'YRY', 'result': 'BBB'},
        ])

        # word, game_log = play.play(
        #     'cot',
        #     words,
        #     opponent.get_potential_next_guesses,
        #     player.get_next_guess,
        #     opponent.get_response,
        #     opponent.GameLog()
        # )
        #
        # self.assertEqual(word, 'cot')
