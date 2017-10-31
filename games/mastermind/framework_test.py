import unittest

from games import code_words
from games.mastermind import opponent, word_generator
from games.mastermind import export_gamelog, analyze_strategy


class FrameworkTests(unittest.TestCase):
    def test_analyze_strategy(self):
        responses = [
            'WWW',  # 03
            'WW',  # 02
            'W',  # 01
            '',  # 00
            'BWW',  # 12
            'BW',  # 21
            'B',  # 10
            'BB',  # 20
            'BBB'  # 30
        ]
        index = {r: i for i, r in enumerate(responses)}

        strategy = {
            '': [
                27,
                '112',
                [
                    [3, '122', [1, 0, 0, 0, 1, 1, 0, 0, 0]],
                    1,
                    [3, '122', [0, 1, 0, 0, 0, 1, 1, 0, 0]],
                    1,
                    [2, '121', [0, 0, 0, 0, 1, 0, 0, 0, 1]],
                    [4, '122', [1, 0, 1, 0, 0, 0, 1, 1, 0]],
                    [6, '133', [0, 1, 0, 1, 1, 1, 1, 0, 1]],
                    [6, 'A'],
                    1,
                ]
            ],
            'A': [
                6,
                '122',
                [
                    0,
                    0,
                    0,
                    0,
                    1,
                    1,
                    [2, '111', [0, 0, 0, 0, 0, 0, 0, 1, 1]],
                    1,
                    1
                ]
            ]
        }

        all_words = word_generator.generate_words('123', 3)

        metrics = analyze_strategy.analyze(all_words, strategy, index, response_sentinel='BBB')

        self.assertEqual(metrics['total_guesses'], 75)

    def test_game_log_to_strategy_one_game(self):
        responses = [
            'WW',  # 02
            'W',  # 01
            '',  # 00
            'B',  # 10
            'BB',  # 20
        ]
        index = {r: i for i, r in enumerate(responses)}

        game_log = [
            {"log": [
                {"guess": ["12", {}], "result": "W"},
                {"guess": ["11", {}], "result": "B"},
                {"guess": ["31", {}], "result": "BB"}
            ]},
        ]

        actual = export_gamelog.export(game_log, index, response_sentinel='BB')
        self.assertEqual(actual, [1, '12', [
            0,
            [1, '11', [0, 0, 0, [1, '31', [0, 0, 0, 0, 1]], 0]],
            0,
            0,
            0
        ]])

    def test_game_log_to_strategy_partial(self):
        responses = [
            'WW',  # 02
            'W',  # 01
            '',  # 00
            'B',  # 10
            'BB',  # 20
        ]
        index = {r: i for i, r in enumerate(responses)}

        game_log = [
            {"log": [
                {"guess": ["12", {}], "result": "W"},
                {"guess": ["11", {}], "result": "B"},
                {"guess": ["31", {}], "result": "BB"}
            ]},
            {"log": [
                {"guess": ["12", {}], "result": "W"},
                {"guess": ["11", {}], "result": ""},
                {"guess": ["23", {}], "result": "BB"}
            ]},
        ]

        actual = export_gamelog.export(game_log, index, response_sentinel='BB')
        self.assertEqual(actual, [2, '12', [
            0,
            [2, '11', [0, 0, [1, '23', [0, 0, 0, 0, 1]], [1, '31', [0, 0, 0, 0, 1]], 0]],
            0,
            0,
            0
        ]])

    def test_game_log_to_strategy_first_guess(self):
        responses = [
            'WW',  # 02
            'W',  # 01
            '',  # 00
            'B',  # 10
            'BB',  # 20
        ]
        index = {r: i for i, r in enumerate(responses)}
        game_log = [
            {"log": [
                {"guess": ["12", {}], "result": "BB"}
            ]},
        ]

        expected = [1, '12', [0, 0, 0, 0, 1]]
        actual = export_gamelog.export(game_log, index, response_sentinel='BB')
        self.assertEqual(actual, expected)

    def test_game_log_to_strategy(self):
        responses = [
            'WW',  # 02
            'W',  # 01
            '',  # 00
            'B',  # 10
            'BB',  # 20
        ]
        index = {r: i for i, r in enumerate(responses)}
        game_log = [
            {"log": [
                {"guess": ["12", {}], "result": "B"},
                {"guess": ["13", {}], "result": "BB"}
            ]},
            {"log": [
                {"guess": ["12", {}], "result": "BB"}
            ]},
            {"log": [
                {"guess": ["12", {}], "result": ""},
                {"guess": ["33", {}], "result": "BB"}
            ]},
            {"log": [
                {"guess": ["12", {}], "result": "B"},
                {"guess": ["13", {}], "result": "B"},
                {"guess": ["11", {}], "result": "BB"}
           ]},
            {"log": [
                {"guess": ["12", {}], "result": "WW"},
                {"guess": ["21", {}], "result": "BB"}
            ]},
            {"log": [
                {"guess": ["12", {}], "result": "B"},
                {"guess": ["13", {}], "result": ""},
                {"guess": ["22", {}], "result": "BB"}
            ]},
            {"log": [
                {"guess": ["12", {}], "result": "B"},
                {"guess": ["13", {}], "result": "W"},
                {"guess": ["32", {}], "result": "BB"}
            ]},
            {"log": [
                {"guess": ["12", {}], "result": "W"},
                {"guess": ["11", {}], "result": "B"},
                {"guess": ["31", {}], "result": "BB"}
            ]},
            {"log": [
                {"guess": ["12", {}], "result": "W"},
                {"guess": ["11", {}], "result": ""},
                {"guess": ["23", {}], "result": "BB"}
            ]},
        ]

        expected = [9, '12', [
            [1, '21', [0, 0, 0, 0, 1]],
            [2, '11', [0, 0, [1, '23', [0, 0, 0, 0, 1]], [1, '31', [0, 0, 0, 0, 1]], 0]],
            [1, '33', [0, 0, 0, 0, 1]],
            [4, '13', [0, [1, '32', [0, 0, 0, 0, 1]], [1, '22', [0, 0, 0, 0, 1]], [1, '11', [0, 0, 0, 0, 1]], 1]],
            1
        ]]
        actual = export_gamelog.export(game_log, index, response_sentinel='BB')
        self.assertEqual(actual, expected)

        all_words = word_generator.generate_words('123', 2)
        metrics = analyze_strategy.analyze(all_words, {'': expected}, index, response_sentinel='BB')
        self.assertEqual(metrics['total_guesses'], 22)

        expected = [9, '12', [
            1,
            [2, '11', [0, 0, 1, 1, 0]],
            [1, '33', [0, 0, 0, 0, 1]],
            [4, '13', [0, 1, 1, 1, 1]],
            1
        ]]

        all_words = word_generator.generate_words('123', 2)
        metrics = analyze_strategy.analyze(all_words, {'': expected}, index, response_sentinel='BB')
        self.assertEqual(metrics['total_guesses'], 22)

        strategy = [9, '12', [[1, '21', [0, 0, 0, 0, 1]], [2, '11', [0, 0, [1, '23', [0, 0, 0, 0, 1]], [1, '31', [0, 0, 0, 0, 1]], 0]], [1, '33', [0, 0, 0, 0, 1]], [4, '13', [0, [1, '32', [0, 0, 0, 0, 1]], [1, '22', [0, 0, 0, 0, 1]], [1, '11', [0, 0, 0, 0, 1]], 1]], 1]]
        metrics = analyze_strategy.analyze(all_words, {'': strategy}, index, response_sentinel='BB')
        self.assertEqual(metrics['total_guesses'], 22)

