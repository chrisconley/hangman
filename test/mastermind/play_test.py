from collections import defaultdict
import random
import unittest

from games import play, code_words, player_utils
from games.mastermind import player, opponent, word_generator
from games import mastermind_play


class MastermindPlayTests(unittest.TestCase):
    def setUp(self):
        play.GUESS_CACHE = {}

    def test_play_short(self):
        words = code_words.Dictionary(['YYY', 'YYR', 'YRY', 'RYY', 'YRR', 'RYR', 'RRY', 'RRR'])
        word, game_log = play.play(
            'YRY',
            words,
            opponent.get_potentials,
            player.build_strategy({'info': 1.0}, model=player_utils.weighted_sum),
            opponent.get_response,
            opponent.GameLog(),
        )

        self.assertEqual(word, 'YRY')
        self.assertEqual(game_log, [
            {'guess': 'RRY', 'result': 'BB'},
            {'guess': 'RYY', 'result': 'BWW'},
            {'guess': 'YRY', 'result': 'BBB'},
        ])

        word, game_log = play.play(
            'RRR',
            words,
            opponent.get_potentials,
            player.build_strategy({'info': 1.0}, model=player_utils.weighted_sum),
            opponent.get_response,
            opponent.GameLog(),
        )

        self.assertEqual(word, 'RRR')
        self.assertEqual(game_log, [
            {'guess': 'RRY', 'result': 'BB'},
            {'guess': 'RYY', 'result': 'B'},
            {'guess': 'RRR', 'result': 'BBB'},
        ])

    def test_play_entropy_alternative(self):
        random.seed(123)
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)
        word, game_log = play.play(
            '3632',
            dictionary,
            opponent.get_potentials,
            player.build_strategy({'info': 1.0}, model=player_utils.weighted_sum),
            opponent.get_response_alternative,
            opponent.GameLog(),
        )

        self.assertEqual(word, '3632')
        self.assertEqual(game_log, [
            {'guess': '1234', 'result': 'BW'},
            {'guess': '1356', 'result': 'WW'},
            {'guess': '2215', 'result': 'W'},
            {'guess': '3544', 'result': 'B'},
            {'guess': '3133', 'result': 'BB'},
            {'guess': '3632', 'result': 'BBBB'},
        ])

    def test_play_minimax_alternative_response(self):
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)
        word, game_log = play.play(
            '3632',
            dictionary,
            opponent.get_potentials,
            player.build_strategy({'minimax': 1.0}, model=player_utils.weighted_sum, should_sort=True),
            opponent.get_response_alternative,
            opponent.GameLog(),
        )

        self.assertEqual(word, '3632')
        self.assertEqual(game_log, [
            {'guess': '1122', 'result': 'B'},
            {'guess': '1334', 'result': 'BW'},
            {'guess': '1456', 'result': 'W'},
            {'guess': '3325', 'result': 'BWW'},
            {'guess': '3632', 'result': 'BBBB'},
        ])

    def test_play_minimax(self):
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)
        word, game_log = play.play(
            '3632',
            dictionary,
            opponent.get_minimax_potentials,
            player.build_strategy({'minimax': 1.0}, model=player_utils.weighted_sum, should_sort=True),
            opponent.get_response,
            opponent.GameLog(),
        )

        self.assertEqual(game_log, [
            {'guess': '1123', 'result': 'WW'},
            {'guess': '2432', 'result': 'BB'},
            {'guess': '3522', 'result': 'BB'},
            {'guess': '1116', 'result': 'W'},
            {'guess': '3632', 'result': 'BBBB'},
        ])

    def test_play_minimax_knuth(self):
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)

        word, game_log = play.play(
            '3632',
            dictionary,
            opponent.get_potentials,
            player.build_knuth_strategy(),
            opponent.get_response_alternative,
            opponent.GameLog(),
        )

        for t in game_log:
            print(t)

        # From http://www.cs.uni.edu/~wallingf/teaching/cs3530/resources/knuth-mastermind.pdf
        self.assertEqual(game_log, [
            {'guess': '1122', 'result': 'B'},
            {'guess': '1344', 'result': 'W'},
            {'guess': '3526', 'result': 'BWW'},
            {'guess': '1162', 'result': 'BW'}, # In Knuth's paper, this guess is 1462
            {'guess': '3632', 'result': 'BBBB'},
        ])

    def test_play_minimax_knuth_all(self):
        all_words = word_generator.generate_words('123456', 4)
        dictionary = code_words.Dictionary(all_words)

        guesses = []
        for codeword in all_words:
            word, game_log = play.play(
                codeword,
                dictionary,
                opponent.get_potentials,
                player.build_knuth_strategy(),
                opponent.get_response_alternative,
                opponent.GameLog(),
            )
            guesses.append(len(game_log))



        # for t in game_log:
        #     print(t)

        # From http://www.cs.uni.edu/~wallingf/teaching/cs3530/resources/knuth-mastermind.pdf
        print('max', max(guesses))
        self.assertEqual(sum(guesses), 5900)

    def test_knuth_44(self):
        forty_four = {'1634', '4426', '6626', '3166', '1645', '5623', '5134', '5342', '6155', '1434', '6134', '6523', '5164', '6154', '1453', '6352', '6326', '3154', '5562', '6342', '5423', '5135', '5426', '1656', '5523', '1564', '4552', '6432', '6524', '3136', '3532', '1635', '1465', '1565', '1335', '3432', '3562', '1655', '4624', '5156', '6165', '6442', '6562', '1435', '3163', '3642', '1554', '1636', '1543', '3424', '5452', '1363', '4165', '1455', '4432', '6145', '5552', '5145', '4136', '4145', '4163', '6426', '5324', '5526', '6424', '1353', '6625', '3323', '5432', '1665', '1534', '4146', '6324', '3632', '4532', '6642', '1566', '5326', '6362', '4324', '3342', '1536', '4423', '6423', '6133', '4526', '6662', '6144', '1445', '5323', '1346', '4326', '4442', '4642', '5462', '1333', '4144', '1563', '3425', '1354', '6146', '4524', '4542', '6623', '3452', '6652', '5143', '6136', '3525', '3362', '1643', '3626', '4155', '4153', '5325', '1343', '1436', '3133', '4134', '1644', '5163', '3326', '4623', '3423', '1356', '1454', '3165', '6425', '3625', '5155', '1364', '3156', '4164', '4452', '5442', '6323', '1334', '1666', '1443', '3325', '4662', '3324', '3145', '1556', '4626', '5542', '4166', '6325', '6624', '1555', '1535', '4362', '5424', '4525', '5362', '5166', '5332', '6166', '1664', '4154', '3652', '3662', '5136', '3552', '4133', '6143', '3164', '4342', '5352', '3542', '4332', '1545', '4325', '3352', '3624', '4523', '5524', '5532', '5625', '6632', '6332', '1663', '1654', '4562', '1463', '1544', '6164', '5165', '1365', '3523', '5652', '1546', '3623', '4156', '4143', '6153', '4135', '6156', '5154', '1336', '5624', '1446', '1456', '4424', '1464', '6452', '1345', '3526', '5626', '4425', '1433', '6525', '6532', '3134', '1553', '1653', '1344', '3332', '3143', '1533', '3462', '1444', '3426', '5642', '3144', '6526', '5153', '5525', '4352', '4625', '1366', '5133', '5144', '4652', '4323', '4462', '4632', '3146', '3155', '6135', '6462', '6552', '1355', '1646', '5425', '1466', '3153', '3442', '5632', '6163', '5662', '6542', '1633', '5146', '3135', '3524'}
        all_guesses = word_generator.generate_words('123456', 4)
        index = mastermind_play.get_index(4)
        for word_guess in all_guesses:
            responses = [0] * len(index)
            for actual_word in forty_four:
                response = opponent.get_response_alternative(actual_word, word_guess)
                responses[index[response]] += 1
            if max(responses) < 39:
                print('$$$$', word_guess, responses)
            if word_guess in {'1344'}:
                print('####', word_guess, word_guess in forty_four, responses)

        print('--------------------------')


        forty_four = {'4562', '4625', '6532', '4652', '4662', '3626', '4626', '3632', '3526', '3552', '3532', '5623', '6462', '3523', '3525', '3625', '5426', '5155', '3623', '6155', '6426', '5425', '5462', '6425', '5156', '6165', '3562', '6623', '3662', '6632', '5452', '6452', '4552', '5632', '4525', '4526', '3652', '5165', '5166', '5523', '5532', '6156', '6166', '6523'}
        all_guesses = word_generator.generate_words('123456', 4)
        index = mastermind_play.get_index(4)
        for word_guess in all_guesses:
            responses = [0]*len(index)
            for actual_word in forty_four:
                response = opponent.get_response_alternative(actual_word, word_guess)
                responses[index[response]] += 1
            if max(responses) < 7:
                print('$$$$', word_guess, responses)
            if word_guess in {'1525', '3526'}:
                print('####', word_guess, word_guess in forty_four, responses)
