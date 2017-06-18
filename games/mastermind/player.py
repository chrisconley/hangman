from collections import Counter, defaultdict, OrderedDict
from decimal import Decimal

from games import entropy
from games.mastermind import opponent
from games.player_utils import get_actual_next_guess


class OrderedCounter(Counter, OrderedDict):
    pass


# TODO: Implement this
def _get_pmf_for_success(possible_responses):
    return {'*': Decimal(1.0)}


def _get_pmf_for_entropy(possible_responses):
    counter = OrderedCounter()
    seen_words = set()
    for response, code_words in possible_responses.items():
        assert code_words.isdisjoint(seen_words), 'There should not be duplicate code words across responses'
        seen_words |= code_words
        counter[response] = Decimal(len(code_words))
    return entropy.get_pmf(counter)


def _get_counts(potential_outcomes):
    common = {}
    entropies = {}
    minimax = {}
    for guess, possible_responses in potential_outcomes.items():
        common_pmf = _get_pmf_for_success(possible_responses)
        common[guess] = common_pmf['*']
        entropy_pmf = _get_pmf_for_entropy(possible_responses)
        minimax[guess] = entropy.get_inverse_minimax(entropy_pmf)
        entropies[guess] = entropy.get_entropy(entropy_pmf)

    results = {}
    results['common'] = common
    results['entropies'] = entropies
    results['minimax'] = minimax
    return results


def build_strategy(info_focus, success_focus, minimax_focus=0.0, final_word_guess=True):

    def strategy(potential_outcomes, game_log):
        data = _get_counts(potential_outcomes)

        if len(potential_outcomes.all_code_words) == 1:
            return list(potential_outcomes.all_code_words)[0]

        common = data.get('common')
        entropies = data.get('entropies')
        minimax = data.get('minimax')

        choices = {}
        for letter, pmf in entropies.items():
            if common[letter] == 0.0 and success_focus == 0.0:
                common_weight = 1
            else:
                common_weight = common[letter]**Decimal(success_focus)
            if entropies[letter] == Decimal(0) and info_focus == 0.0:
                entropy_weight = 1
            else:
                entropy_weight = entropies[letter]**Decimal(info_focus)
            if minimax[letter] == Decimal(0) and minimax_focus == 0.0:
                minimax_weight = 1
            else:
                minimax_weight = minimax[letter]**Decimal(minimax_focus)
            choices[letter] = entropy_weight * common_weight * minimax_weight

        next_guess = get_actual_next_guess(choices, game_log)
        return next_guess

    return strategy
