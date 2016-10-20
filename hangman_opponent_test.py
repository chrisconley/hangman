import unittest

from hangman_opponent import HangmanGameState


class HangmanGameStateTests(unittest.TestCase):
    def test_string(self):
        state = HangmanGameState('banana', set())
        self.assertEqual(state, '------')

        state = HangmanGameState('banana', set('c'))
        self.assertEqual(state, '------')

        state = HangmanGameState('banana', set('cbn'))
        self.assertEqual(state, 'b-n-n-')

    def test_missed_letters(self):
        state = HangmanGameState('banana', set())
        self.assertEqual(state.missed_letters, set())

        state = HangmanGameState('banana', set('bn'))
        self.assertEqual(state.missed_letters, set())

        state = HangmanGameState('banana', set('bnce'))
        self.assertEqual(state.missed_letters, set('ce'))

    def test_known_letters(self):
        state = HangmanGameState('banana', set())
        self.assertEqual(state.known_letters, set())

        state = HangmanGameState('banana', set('bn'))
        self.assertEqual(state.known_letters, set('bn'))

        state = HangmanGameState('banana', set('bnce'))
        self.assertEqual(state.known_letters, set('bn'))