from games import entropy
from games.player_utils import build_strategy as generic_build_strategy
from games.player_utils import OrderedCounter, Decimal


def _get_pmf_for_success(possible_responses):
    counter = OrderedCounter()
    successful_code_words = set()
    seen_words = set()
    for response, code_words in possible_responses.items():
        assert code_words.isdisjoint(seen_words), 'There should not be duplicate code words across responses'
        seen_words |= code_words
        if response == '!':
            counter['!'] = Decimal(len(code_words))
        else:
            successful_code_words |= code_words
    counter['*'] = Decimal(len(successful_code_words))
    return entropy.get_pmf(counter)


def build_strategy(foci, model, should_sort=False):
    return generic_build_strategy(
        foci=foci,
        model=model,
        reward_pmf=_get_pmf_for_success,
        should_sort=should_sort)


def get_next_guess_naive(potentials, game_log):
    # If we've whittled down to return one remaining word,
    # return that word as our next guess to finish the game.
    if potentials.total_length == 1:
        return list(potentials.all_code_words)[0]

    potential_guesses = 'esiarntolcdupmghbyfvkwzxqj'
    worthwhile_guesses = set(''.join(potentials.all_code_words))
    for guess in potential_guesses:
        if guess in game_log.guesses or guess not in worthwhile_guesses:
            continue
        return guess
