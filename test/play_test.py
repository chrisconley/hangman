from decimal import Decimal
import unittest

from games import play, player_utils


class PlayTests(unittest.TestCase):
    def test_game_log_as_json(self):
        ris = play.RIS(
            model='weighted_og',
            foci={'info': 1.0, 'reward': 0.0})
        game_log = [
            {'guess': player_utils.Guess('c', {'info': Decimal(2)}), 'result': '!'},
            {'guess': player_utils.Guess('e', {'info': Decimal(3)}), 'result': '-c--'},
        ]
        as_json = play.game_log_as_json('hangman', ris, game_log, seed=123)

        self.assertEqual(as_json, {
            'game': 'hangman',
            'seed': 123,
            'strategy': {
                'model': 'weighted_og',
                'foci': {'info': 1.0, 'reward': 0.0}
            },
            'log': [
                {
                    'guess': ['c', {'info': 2}],
                    'result': '!'
                },
                {
                    'guess': ['e', {'info': 3}],
                    'result': '-c--'
                },
            ]
        })
        self.assertEqual(type(as_json['log'][0]['guess'][1]['info']), float)

