from games.player_utils import build_strategy as generic_build_strategy
from games.player_utils import OrderedCounter, Decimal


# TODO: Implement this
def _get_pmf_for_success(possible_responses):
    return {'*': Decimal(1.0)}


def build_knuth_strategy():
    minimax_strategy = build_strategy(
        info_focus=0.0,
        success_focus=0.0,
        minimax_focus=1.0,
        should_sort=True)

    def strategy(potential_outcomes, game_log):
        if len(game_log) == 0:
            return '1122'
        else:
            return minimax_strategy(potential_outcomes, game_log)
    return strategy


def build_strategy(info_focus, success_focus, minimax_focus=0.0, should_sort=False):
    return generic_build_strategy(
        info_focus=info_focus,
        success_focus=success_focus,
        minimax_focus=minimax_focus,
        success_pmf=_get_pmf_for_success,
        should_sort=should_sort)
