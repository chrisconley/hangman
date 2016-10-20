import random

from play import get_actual_next_guess
import battleship_opponent as battleship

# guess = get_actual_next_guess(game_state, choices)


def get_next_guess(game_state):
    spots = set(range(0, len(game_state)))
    remaining_choices = spots - game_state.guesses
    return random.choice(list(remaining_choices))

if __name__ == '__main__':
    from argparse import ArgumentParser
    import fileinput

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    args = parser.parse_args()

    random.seed(15243)

    words = [word.strip() for word in fileinput.input(args.file)]

    for word in words:
        game = battleship.play(word.strip())
        for game_state in game:
            next_guess = get_next_guess(game_state)
            print(next_guess, game_state)
            try:
                game.send(next_guess)
            except StopIteration:
                pass
            result = battleship.BattleShipGameState(
                word,
                (set(game_state.guesses) | set([next_guess]))
            )
        print('---', word, result)