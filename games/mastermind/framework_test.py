import unittest

from games import code_words
from games.mastermind import opponent, word_generator


class FrameworkTests(unittest.TestCase):
    def test_it(self):
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
        dictionary = code_words.Dictionary(all_words)

        def play(code_word):
            guesses = []
            strategy_place = strategy['']
            while True:
                if type(strategy_place) == int and strategy_place == 1:
                    guesses.append('gotit')
                    break
                if strategy_place[1] < 'A':
                    guess = strategy_place[1]
                else:
                    strategy_place = strategy[strategy_place[1]]
                    guess = strategy_place[1]
                response = opponent.get_response(code_word, guess)

                strategy_place = strategy_place[2][index[response]]
                guesses.append(guess)
                if response == 'BBB':
                    break
            return guesses

        total_guesses = 0
        for word in all_words:
            guesses = play(word)
            total_guesses += len(guesses)

        self.assertEqual(total_guesses, 75)

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
            ]},
        ]

        actual = export(game_log, index)
        self.assertEqual(actual, [1, '12', [0, 1, 0, 0, 0]])

        game_log = [
            {"log": [
                {"guess": ["12", {}], "result": "W"},
                {"guess": ["11", {}], "result": "B"},
            ]},
        ]

        actual = export(game_log, index)
        self.assertEqual(actual, [1, '12', [0, 1, 0, 0, 0]])

        game_log = [
            {"log": [
                {"guess": ["12", {}], "result": "W"},
                {"guess": ["11", {}], "result": "B"},
                {"guess": ["31", {}], "result": "BB"}
            ]}
        ]

        actual = export(game_log, index)
        self.assertEqual(actual, [1, '12', [0, 1, 0, 0, 0]])

        game_log = [
            {"log": [
                {"guess": ["12", {}], "result": "W"},
                {"guess": ["11", {}], "result": "B"},
                # {"guess": ["31", {}], "result": "BB"}
            ]},
            {"log": [
                {"guess": ["12", {}], "result": "W"},
                {"guess": ["11", {}], "result": ""},
                # {"guess": ["23", {}], "result": "BB"}
            ]},
        ]

        actual = export(game_log, index)
        self.assertEqual(actual, [2, '12', [0, [2, '11', [0, 0, 1, 1, 0]], 0, 0, 0]])

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

        expected = [
            9,
            '12',
            [
                1,  # WW
                [2, '11', [0, 0, 1, 1, 0]],  # W
                1,  #
                [4, '13', [0, 1, 1, 1, 1]],  # B
                1,  # BB
            ]
        ]
        actual = export(game_log, index)
        self.assertEqual(actual, expected)


def get_new_leaf(index):
    return [0, '', [0]*len(index)]


def export(game_log, index):
    strategy = get_new_leaf(index)
    for game in game_log:
        current_place = strategy
        for turn in game['log']:
            response_index = index[turn['result']]
            if current_place == 1:
                current_place = get_new_leaf(index)
                # current_place[0] += 1
            current_place[0] += 1
            current_place[1] = turn['guess'][0]

            # print('---', current_place)
            # print(current_place)
            if current_place[2][response_index] == 0:
                # print('yyyyyyy')
                current_place[2][response_index] += 1
            elif current_place[2][response_index] == 1:
                # print('xxxxxxx')
                current_place[2][response_index] = get_new_leaf(index)
                current_place[2][response_index][0] = 1
                # current_place[2][response_index][1] = turn['guess'][0]
                # print(current_place)
            else:
                print('RRRR', current_place[2][response_index])
                print(turn)
                # current_place[0] += 1
                # current_place[2][response_index][0] += 1

            # print('///', current_place)
            current_place = current_place[2][response_index]
            # print('~~~', current_place)


    print(strategy)
    return strategy
