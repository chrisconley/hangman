import unittest

from games.hangman import opponent


class HangmanOpponentTests(unittest.TestCase):
    def test_get_response(self):
        opponent.clear_cache()
        result = opponent.get_response('cat', 't')
        self.assertEqual(result, '--t')

        opponent.clear_cache()
        result = opponent.get_response('cat', 's')
        self.assertEqual(result, '!')

        opponent.clear_cache()
        result = opponent.get_response('cat', 'cat')
        self.assertEqual(result, 'cat')

        opponent.clear_cache()
        result = opponent.get_response('cat', 'can')
        self.assertEqual(result, '!')


class HangmanPotentialsTests(unittest.TestCase):
    def test_get_potentials(self):
        words = ['cat', 'bat']
        potentials = opponent.get_potentials(words, opponent.get_response, opponent.GameLog())
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


class PossibleResponsesTests(unittest.TestCase):
    def test_initialization(self):
        result = opponent.PossibleResponses(guess='c')
        self.assertEqual(result, {})
        self.assertEqual(result.guess, 'c')

        result = opponent.PossibleResponses(guess='c')
        self.assertEqual(result['random response'], set())

    def test_as_counts(self):
        possible_responses = opponent.PossibleResponses(guess='c')
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
        possible_responses = opponent.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar'}
        })

        self.assertEqual(possible_responses.guess, 'c')
        self.assertEqual(possible_responses['c--'], {'cat'})
        self.assertEqual(possible_responses['!'], {'bar', 'tab', 'tar'})


class PotentialGuessesTests(unittest.TestCase):
    def test_initialization(self):
        potential_guesses = opponent.PotentialOutcomes()
        self.assertEqual(potential_guesses, {})

        potential_guesses = opponent.PotentialOutcomes({'c': {'c--': {'cat'}}})
        possible_response = potential_guesses.get('c')

        self.assertEqual(type(possible_response), opponent.PossibleResponses)
        self.assertEqual(possible_response.guess, 'c')
        self.assertEqual(possible_response['c--'], {'cat'})

        self.assertEqual(potential_guesses.all_code_words, {'cat'})

    def test_add(self):
        potential_guesses = opponent.PotentialOutcomes()
        potential_guesses.add('c', 'c--', 'cat')
        possible_response = potential_guesses.get('c')

        self.assertEqual(type(possible_response), opponent.PossibleResponses)
        self.assertEqual(possible_response.guess, 'c')
        self.assertEqual(possible_response['c--'], {'cat'})

        self.assertEqual(potential_guesses.all_code_words, {'cat'})

    def test_get_by_guess_response(self):
        potential_guesses = opponent.PotentialOutcomes()
        potential_guesses.add('c', 'c--', 'cat')
        self.assertEqual(potential_guesses.get_by_guess_response('c', 'c--'), {'cat'})

    def test_guesses(self):
        potential_guesses = opponent.PotentialOutcomes()
        potential_guesses.add('c', 'c--', 'cat')
        self.assertEqual(potential_guesses.guesses, {'c'})
