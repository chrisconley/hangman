import unittest

import dictionary
import hangman


class HangmanTests(unittest.TestCase):
    def test_string(self):
        state = hangman.GameState('banana', set())
        self.assertEqual(state, '------')

        state = hangman.GameState('banana', set('c'))
        self.assertEqual(state, '------')

        state = hangman.GameState('banana', set('cbn'))
        self.assertEqual(state, 'b-n-n-')

    def test_missed_letters(self):
        state = hangman.GameState('banana', set())
        self.assertEqual(state.missed_letters, set())

        state = hangman.GameState('banana', set('bn'))
        self.assertEqual(state.missed_letters, set())

        state = hangman.GameState('banana', set('bnce'))
        self.assertEqual(state.missed_letters, set('ce'))

    def test_known_letters(self):
        state = hangman.GameState('banana', set())
        self.assertEqual(state.known_letters, set())

        state = hangman.GameState('banana', set('bn'))
        self.assertEqual(state.known_letters, set('bn'))

        state = hangman.GameState('banana', set('bnce'))
        self.assertEqual(state.known_letters, set('bn'))

    def test_apply_guess(self):
        original_state = hangman.GameState('banana', guesses=[])
        next_state = hangman.apply_guess(original_state, 'a')
        self.assertEqual(next_state, '-a-a-a')

    def test_play(self):
        def get_next_guess(game_state, dictionary):
            letters = 'zcnat'
            for letter in letters:
                if letter not in game_state.guesses:
                    return letter
        game_state, game_log = hangman.play('cat', get_next_guess, encoded_dictionary='mock')

        self.assertEqual(game_state, 'cat')
        self.assertEqual(game_log, [
            {
                'guess': 'z',
                'result': False
            },
            {
                'guess': 'c',
                'result': True
            },
            {
                'guess': 'n',
                'result': False
            },
            {
                'guess': 'a',
                'result': True
            },
            {
                'guess': 't',
                'result': True
            },
        ])

    def test_play_with_correct_word_guess(self):
        def get_next_guess(game_state, encoded_dictionary):
            rejected_letters = game_state.missed_letters # Why do we need to pass this in explicitly?
            remaining_words = dictionary.filter_words(encoded_dictionary, game_state, rejected_letters)
            if len(remaining_words) == 1:
                return remaining_words[0]

            letters = 'zcnat'
            for letter in letters:
                if letter not in game_state.guesses:
                    return letter

        encoded_dictionary = dictionary.encode_dictionary(['cat', 'bat', 'can'])
        game_state, game_log = hangman.play('cat', get_next_guess, encoded_dictionary=encoded_dictionary)

        self.assertEqual(game_state, 'cat')
        self.assertEqual(game_log, [
            {
                'guess': 'z',
                'result': False
            },
            {
                'guess': 'c',
                'result': True
            },
            {
                'guess': 'n',
                'result': False
            },
            {
                'guess': 'cat',
                'result': True
            },
        ])

