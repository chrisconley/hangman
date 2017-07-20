import random
import unittest

from bitarray import bitarray

from games import code_words


class CodeWordsDictionaryTests(unittest.TestCase):
    def test_get_partial_dictionary(self):
        dictionary = code_words.Dictionary(['cat', 'bat'])
        result = dictionary.get_partial_dictionary({'bat'})
        self.assertEqual(result.as_bits, bitarray('01'))
        self.assertEqual(result.as_words, {'bat'})
        self.assertEqual(result.all_words, ['cat', 'bat'])

    def test_words_to_bits(self):
        dictionary = code_words.Dictionary(['cat', 'bat'])
        result = dictionary.words_to_bits({'bat'})
        self.assertEqual(result, bitarray('01'))

        result = dictionary.words_to_bits({'cat'})
        self.assertEqual(result, bitarray('10'))

        result = dictionary.words_to_bits({'bat', 'cat'})
        self.assertEqual(result, bitarray('11'))

    def test_bits_to_words(self):
        dictionary = code_words.Dictionary(['cat', 'bat'])
        result = dictionary.bits_to_words(bitarray('01'))
        self.assertEqual(result, {'bat'})

        result = dictionary.bits_to_words(bitarray('10'))
        self.assertEqual(result, {'cat'})

        result = dictionary.bits_to_words(bitarray('11'))
        self.assertEqual(result, {'cat', 'bat'})


class PossibleResponsesTests(unittest.TestCase):
    def test_initialization(self):
        result = code_words.PossibleResponses(guess='c')
        self.assertEqual(result, {})
        self.assertEqual(result.guess, 'c')

        result = code_words.PossibleResponses(guess='c')
        self.assertEqual(result['random response'], set())

    def test_as_counts(self):
        random.seed(123, version=1)
        possible_responses = code_words.PossibleResponses(guess='c')
        possible_responses['c--'].add('cat')
        possible_responses['c--'].add('can')
        possible_responses['--n'].add('can')
        possible_responses['!'].add('tar')
        possible_responses['!'].add('bus')
        possible_responses['!'].add('fir')
        counts = possible_responses.as_counts()
        self.assertEqual(counts, {
            'c--': 2,
            '--n': 1,
            '!': 3
        })

        self.assertEqual(counts.most_common(), [
            ('!', 3),
            ('c--', 2),
            ('--n', 1),

        ])

    def test_from_dict(self):
        possible_responses = code_words.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar'}
        })

        self.assertEqual(possible_responses.guess, 'c')
        self.assertEqual(possible_responses['c--'], {'cat'})
        self.assertEqual(possible_responses['!'], {'bar', 'tab', 'tar'})

    def test_code_words(self):
        possible_responses = code_words.PossibleResponses.from_dict('c', {
            'c--': {'cat'},
            '-c-': {'ace'},
            '!': {'bar', 'tab', 'tar'}
        })

        self.assertEqual(possible_responses.code_words, {'cat', 'ace', 'bar', 'tab', 'tar'})


class PotentialGuessesTests(unittest.TestCase):
    def test_initialization(self):
        potential_guesses = code_words.PotentialOutcomes()
        self.assertEqual(potential_guesses, {})

        potential_guesses = code_words.PotentialOutcomes({'c': {'c--': {'cat'}}})
        possible_response = potential_guesses.get('c')

        self.assertEqual(type(possible_response), code_words.PossibleResponses)
        self.assertEqual(possible_response.guess, 'c')
        self.assertEqual(possible_response['c--'], {'cat'})

        self.assertEqual(potential_guesses.all_code_words, {'cat'})

    def test_add(self):
        potential_guesses = code_words.PotentialOutcomes()
        potential_guesses.add('c', 'c--', 'cat')
        possible_response = potential_guesses.get('c')

        self.assertEqual(type(possible_response), code_words.PossibleResponses)
        self.assertEqual(possible_response.guess, 'c')
        self.assertEqual(possible_response['c--'], {'cat'})

        self.assertEqual(potential_guesses.all_code_words, {'cat'})

    def test_get_by_guess_response(self):
        potential_guesses = code_words.PotentialOutcomes()
        potential_guesses.add('c', 'c--', 'cat')
        self.assertEqual(potential_guesses.get_by_guess_response('c', 'c--'), {'cat'})

    def test_guesses(self):
        potential_guesses = code_words.PotentialOutcomes()
        potential_guesses.add('c', 'c--', 'cat')
        self.assertEqual(potential_guesses.guesses, {'c'})
