import random
import unittest

import dictionary
import hangman
import hangman_players


class HangmanPlayersTests(unittest.TestCase):
    def test_max_info_gain(self):
        random.seed(15243)
        words = ['scrabbler', 'scrambler', 'scratcher', 'scrounger',
                 'straddler', 'straggler', 'strangler', 'struggler'
                 ]
        encoded_dictionary = dictionary.encode_dictionary(words)

        game_state = hangman.GameState('scrabbler', set('srei'))
        next_guess = hangman_players.entropy_next_guess(game_state, encoded_dictionary)

        self.assertEqual(next_guess, 'g')

        # scorer = scorers.build_multiplier_scorer(0, 1)
        # next_guess = play.entropy_strategy(game_state, counts, len(words), scorer)
        #
        # self.assertEqual(next_guess, 't')

        next_guess = hangman_players.most_common(game_state, encoded_dictionary)
        self.assertEqual(next_guess, 'a')