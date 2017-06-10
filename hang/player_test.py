from decimal import Decimal
import random
import unittest
from unittest.mock import patch

from hang import opponent, player, play


class HangmanPlayerTests(unittest.TestCase):
    def assertDecimalAlmostEqual(self, actual, expected, places):
        self.assertEqual(type(actual), Decimal)
        self.assertAlmostEqual(float(actual), float(expected), places=places)

    def test_build_strategy(self):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        game_log = play.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r-----r'},
            {'guess': 'e', 'result': '-------e-'},
            {'guess': 'i', 'result': '!'},
        ])
        potentials = player.get_potentials(words, opponent.get_response, game_log)

        strategy = player.build_strategy(info_focus=1.0, success_focus=0.0, final_word_guess=True)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'g')

        strategy = player.build_strategy(0.5, 0.5, final_word_guess=True)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 't')

        strategy = player.build_strategy(info_focus=0.0, success_focus=1.0, final_word_guess=True)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'a')

    def test_build_strategy_final_word_guess(self):
        random.seed(15243)
        words = ['scrabbler']
        game_log = play.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r-----r'},
            {'guess': 'e', 'result': '-------e-'},
            {'guess': 'i', 'result': '!'},
        ])
        potentials = player.get_potentials(words, opponent.get_response, game_log)

        strategy = player.build_strategy(info_focus=1.0, success_focus=0.0, final_word_guess=True)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'scrabbler')

    def test_get_potentials(self):
        words = ['cat', 'bat']
        potentials = player.get_potentials(words, opponent.get_response, play.GameLog())
        print(potentials)
        self.assertEqual(potentials, {
            'a': {
                '-a-': {'cat', 'bat'}
            },
            'b': {
                'b--': {'bat'}, '!': {'cat'}
            },
            'c': {
                'c--': {'cat'}, '!': {'bat'}
            },
            't': {
                '--t': {'cat', 'bat'}
            }
        })

    def test_get_next_guess_naive(self):
        potentials = player.PotentialOutcomes({
            'a': {
                '-a-': {'cat', 'bat'}
            },
            'b': {
                'b--': {'bat'}, '!': {'cat'}
            },
            'c': {
                'c--': {'cat'}, '!': {'bat'}
            },
            't': {
                '--t': {'cat', 'bat'}
            }
        })
        next_guess = player.get_next_guess_naive(potentials, play.GameLog())
        self.assertEqual(next_guess, 'a')

    def test_get_next_guess_naive_with_game_log(self):
        potentials = player.PotentialOutcomes({
            'b': {
                'b--': {'bat'}, '!': {'cat'}
            },
            'c': {
                'c--': {'cat'}, '!': {'bat'}
            },
            't': {
                '--t': {'cat', 'bat'}
            }
        })
        game_log = play.GameLog([{'guess': 'a', 'result': '-a-'}])
        next_guess = player.get_next_guess_naive(potentials, game_log)
        self.assertEqual(next_guess, 't')

    def test_get_next_guess_naive_with_one_word_left(self):
        potentials = player.PotentialOutcomes({
            'b': {
                'b--': {'bat'}
            },
            'c': {
                '!': {'bat'}
            },
            't': {
                '--t': {'bat'}
            }
        })
        game_log = play.GameLog([{'guess': 'a', 'result': '-a-'}])
        next_guess = player.get_next_guess_naive(potentials, game_log)
        self.assertEqual(next_guess, 'bat')

    def test_get_pmf_for_success(self):
        possible_responses = player.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar'}
        })
        pmf = player._get_pmf_for_success(possible_responses)
        self.assertDecimalAlmostEqual(pmf['*'], Decimal('0.40000000000000'), places=17)
        self.assertDecimalAlmostEqual(pmf['!'], Decimal('0.60000000000000'), places=17)

        possible_responses = player.PossibleResponses.from_dict('d', {
            '!': {'bar', 'tab', 'tar', 'ace', 'cat'}
        })
        pmf = player._get_pmf_for_success(possible_responses)
        self.assertDecimalAlmostEqual(pmf['*'], Decimal('0.00000000000000'), places=17)
        self.assertDecimalAlmostEqual(pmf['!'], Decimal('1.00000000000000'), places=17)

    def test_get_pmf_for_success_raises_if_duplicate_invalid_codewords(self):
        possible_responses = player.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace', 'cat'},
            '!': {'bar', 'tab', 'tar'}
        })
        with self.assertRaises(AssertionError):
            player._get_pmf_for_success(possible_responses)

        possible_responses = player.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar', 'cat'}
        })
        with self.assertRaises(AssertionError):
            player._get_pmf_for_success(possible_responses)

    def test_get_pmf_for_entropy(self):
        possible_responses = player.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar'}
        })
        pmf = player._get_pmf_for_entropy(possible_responses)
        self.assertIsNone(pmf.get('*'))
        self.assertDecimalAlmostEqual(pmf['c--'], Decimal('0.20000000000000'), places=17)
        self.assertDecimalAlmostEqual(pmf['!'], Decimal('0.60000000000000'), places=17)

        possible_responses = player.PossibleResponses.from_dict('d', {
            '!': {'bar', 'tab', 'tar', 'ace', 'cat'}
        })
        pmf = player._get_pmf_for_entropy(possible_responses)
        self.assertIsNone(pmf.get('*'))
        self.assertDecimalAlmostEqual(pmf['!'], Decimal('1.00000000000000'), places=17)
        
    def test_get_pmf_for_entropy_raises_if_duplicate_invalid_codewords(self):
        possible_responses = player.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace', 'cat'},
            '!': {'bar', 'tab', 'tar'}
        })
        with self.assertRaises(AssertionError):
            player._get_pmf_for_entropy(possible_responses)

        possible_responses = player.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar', 'cat'}
        })
        with self.assertRaises(AssertionError):
            player._get_pmf_for_entropy(possible_responses)

    def test_get_cache_key(self):
        game_log = play.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r-----r'},
            {'guess': 'e', 'result': '------e--'},
            {'guess': 'i', 'result': '!'},
            {'guess': 'a', 'result': '!'},
        ])

        cache_key = player._get_cache_key(game_log)
        self.assertEqual(cache_key, 's-r---e-r:ai')

    def test_get_cache_key_when_no_correct_guesses(self):
        game_log = play.GameLog([
            {'guess': 'i', 'result': '!'},
            {'guess': 'a', 'result': '!'},
        ])

        cache_key = player._get_cache_key(game_log)
        self.assertEqual(cache_key, ':ai')

    def test_get_cache_key_when_no_missed_guesses(self):
        game_log = play.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r-----r'},
            {'guess': 'e', 'result': '------e--'},
        ])

        cache_key = player._get_cache_key(game_log)
        self.assertEqual(cache_key, 's-r---e-r:')

    @patch('hang.player.get_actual_next_guess', return_value='hi')
    def test_build_strategy_does_not_cache_counts_by_default(self, get_next_guess):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        game_log = play.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r-----r'},
            {'guess': 'e', 'result': '-------e-'},
            {'guess': 'i', 'result': '!'},
        ])
        potentials = player.get_potentials(words, opponent.get_response, game_log)

        strategy = player.build_strategy(info_focus=1.0, success_focus=0.0, final_word_guess=True)
        next_guess = strategy(potentials, game_log)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'hi')

        self.assertEqual(get_next_guess.call_count, 2)

    @patch('hang.player.get_actual_next_guess', return_value='hi')
    def test_build_strategy_does_cache_counts_when_use_cache_is_true(self, get_next_guess):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        game_log = play.GameLog([
            {'guess': 's', 'result': 's--------'},
            {'guess': 'r', 'result': '--r-----r'},
            {'guess': 'e', 'result': '-------e-'},
            {'guess': 'i', 'result': '!'},
        ])
        potentials = player.get_potentials(words, opponent.get_response, game_log)

        strategy = player.build_strategy(info_focus=1.0, success_focus=0.0, final_word_guess=True, use_cache=True)
        next_guess = strategy(potentials, game_log)
        next_guess = strategy(potentials, game_log)
        self.assertEqual(next_guess, 'hi')

        self.assertEqual(get_next_guess.call_count, 1)


class PossibleResponsesTests(unittest.TestCase):
    def test_initialization(self):
        result = player.PossibleResponses(guess='c')
        self.assertEqual(result, {})
        self.assertEqual(result.guess, 'c')

        result = player.PossibleResponses(guess='c')
        self.assertEqual(result['random response'], set())

    def test_as_counts(self):
        possible_responses = player.PossibleResponses(guess='c')
        possible_responses['c--'].add('cat')
        possible_responses['c--'].add('can')
        possible_responses['--n'].add('can')
        possible_responses['!'].add('tar')
        possible_responses['!'].add('bus')
        counts = possible_responses.as_counts()
        self.assertEqual(counts, {
            'c--': 2,
            '--n': 1,
            '!': 2
        })

        self.assertEqual(counts.most_common(), [
            ('c--', 2),
            ('!', 2),
            ('--n', 1),

        ])

    def test_from_dict(self):
        possible_responses = player.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar'}
        })

        self.assertEqual(possible_responses.guess, 'c')
        self.assertEqual(possible_responses['c--'], {'cat'})
        self.assertEqual(possible_responses['!'], {'bar', 'tab', 'tar'})


class PotentialGuessesTests(unittest.TestCase):
    def test_initialization(self):
        potential_guesses = player.PotentialOutcomes()
        self.assertEqual(potential_guesses, {})

        potential_guesses = player.PotentialOutcomes({'c': {'c--': {'cat'}}})
        possible_response = potential_guesses.get('c')

        self.assertEqual(type(possible_response), player.PossibleResponses)
        self.assertEqual(possible_response.guess, 'c')
        self.assertEqual(possible_response['c--'], {'cat'})

        self.assertEqual(potential_guesses.all_code_words, {'cat'})

    def test_add(self):
        potential_guesses = player.PotentialOutcomes()
        potential_guesses.add('c', 'c--', 'cat')
        possible_response = potential_guesses.get('c')

        self.assertEqual(type(possible_response), player.PossibleResponses)
        self.assertEqual(possible_response.guess, 'c')
        self.assertEqual(possible_response['c--'], {'cat'})

        self.assertEqual(potential_guesses.all_code_words, {'cat'})

    def test_get_by_guess_response(self):
        potential_guesses = player.PotentialOutcomes()
        potential_guesses.add('c', 'c--', 'cat')
        self.assertEqual(potential_guesses.get_by_guess_response('c', 'c--'), {'cat'})

    def test_guesses(self):
        potential_guesses = player.PotentialOutcomes()
        potential_guesses.add('c', 'c--', 'cat')
        self.assertEqual(potential_guesses.guesses, {'c'})
