from games import player_utils
from games.player_utils import Decimal


# TODO: Implement this
def _get_pmf_for_success(possible_responses):
    return {'*': Decimal(1.0)}


def build_knuth_strategy():
    minimax_strategy = build_strategy(
        foci={'minimax': 1.0},
        model=player_utils.weighted_product,
        should_sort=True)

    def strategy(potential_outcomes, game_log):
        if len(game_log) == 0:
            return '1122'
        else:
            return minimax_strategy(potential_outcomes, game_log)
    return strategy


def build_strategy(foci, model, should_sort=False):
    return player_utils.build_strategy(
        foci=foci,
        model=model,
        reward_pmf=_get_pmf_for_success,
        should_sort=should_sort)
