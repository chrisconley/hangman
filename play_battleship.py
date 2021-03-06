from collections import defaultdict
import random

from games.player_utils import get_actual_next_guess, OrderedCounter
import battleship_opponent as battleship
import dictionary
from games import entropy


def count_index_letters(words):
    counts = defaultdict(OrderedCounter)
    counts['*'] = 0
    for word in words:
        for index, letter in enumerate(word):
            counter = counts[str(index)]
            counter[letter] += 1
            counter['*'] += 1
        counts['*'] += 1
    return counts


def get_next_entropy_guess(game_state, words):
    counts = count_index_letters(words)
    entropies = entropy.get_new_entropies(counts)
    return get_actual_next_guess(game_state, entropies)


def get_next_random_guess(game_state):
    spots = set(range(0, len(game_state)))
    remaining_choices = spots - game_state.guesses
    return random.choice(list(remaining_choices))


def get_next_neighbor_guess(game_state):
    """
    This uses knowledge that ships have a length and
    if we have a hit somewhere, then there's a higher likelihood
    that we'll get another hit in an adjacent spot.

    If we don't have any hits with adjacent spots that we haven't
    tested yet, then we fall back to random choice.
    """
    if game_state[0] == '-' and game_state[1] == '1':
        return 0
    if game_state[-1] == '-' and game_state[-2] == '1':
        return len(game_state) - 1

    for index, spot in enumerate(game_state):
        if index == 0 or index == len(game_state)-1:
            continue
        if spot != '-':
            continue
        is_adjacent_to_hit = game_state[index-1] == '1' or game_state[index+1] == '1'
        if is_adjacent_to_hit:
            return index
    return get_next_random_guess(game_state)

if __name__ == '__main__':
    from argparse import ArgumentParser
    import fileinput

    parser = ArgumentParser()
    parser.add_argument('file', help='input words')
    args = parser.parse_args()

    random.seed(15243)

    words = [word.strip() for word in fileinput.input(args.file)]
    encoded_dictionary = dictionary.encode_dictionary(words)
    for key, value in encoded_dictionary.items():
        print(key, value)

    scores = []

    for word in words:
        game = battleship.play(word.strip())
        for game_state in game:
            remaining_words = dictionary.filter_words(encoded_dictionary, game_state, set())
            next_guess = get_next_neighbor_guess(game_state)
            try:
                game.send(next_guess)
            except StopIteration:
                pass
            result = battleship.BattleShipGameState(
                word,
                (set(game_state.guesses) | set([next_guess]))
            )
        print('---', word, result)
        scores.append(len(result.guesses))

    avg = sum(scores) / float(len(scores))
    print('Average Score: ', avg)
