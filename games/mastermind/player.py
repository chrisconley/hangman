from games import player_utils
from games.player_utils import Decimal


def _get_percents(response):
    if len(response) > 4:  # TODO: Fix this - will need to pass in codeword length
        raise RuntimeError('Mastermind codeword of length 4 is only supported')
    result = 0.0
    for character in response:
        if character == 'B':
            result += 0.25
        elif character == 'W':
            result += 0.125
        else:
            raise ValueError('Response must only include "B" or "W"')
    return result


def _get_pmf_for_success(possible_responses):
    total = 0.0
    for response, code_words in possible_responses.items():
        total += _get_percents(response) * len(code_words)
    success_percent = Decimal(total/len(possible_responses.code_words))
    return {
        '*': success_percent,
        '!': Decimal(1.0) - success_percent
    }


def build_knuth_strategy():
    minimax_strategy = build_strategy(
        foci={'minimax': 1.0},
        model=player_utils.weighted_product,
        sorts=[player_utils.valid_sort, player_utils.lexical_sort])

    def strategy(potential_outcomes, game_log):
        if len(game_log) == 0:
            return player_utils.Guess('1122', {}
                                      )
        else:
            return minimax_strategy(potential_outcomes, game_log)
    return strategy


def build_strategy(foci, model, sorts=[]):
    return player_utils.build_strategy(
        foci=foci,
        model=model,
        reward_pmf=_get_pmf_for_success,
        sorts=sorts)
