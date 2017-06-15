from collections import Counter, defaultdict, OrderedDict


class OrderedCounter(Counter, OrderedDict):
    pass


class GameLog(list):
    @property
    def guesses(self):
        return {t['guess'] for t in self}

CACHE = {}


def clear_cache():
    CACHE = {}


def get_response(code_word, guess):
    cache_key = (code_word, guess)
    cached_response = CACHE.get(cache_key)
    if cached_response:
        return cached_response

    if code_word == guess:
        response = code_word
    else:
        response = [
            (letter if (letter == guess) else '-')
            for index, letter
            in enumerate(code_word)]
        if set(response) == {'-'}:
            response = ['!']
        response = ''.join(response)
    CACHE[cache_key] = response
    return response


# TODO: Move potential/possible stuff to opponent
class PossibleResponses(defaultdict):
    def __init__(self, guess):
        self.guess = guess
        super().__init__(set)

    def as_counts(self):
        counter = OrderedCounter()
        for response, code_words in self.items():
            counter[response] = len(code_words)
        return counter

    @classmethod
    def from_dict(cls, guess, data):
        possible_responses = cls(guess)
        for response, code_words in data.items():
            possible_responses[response] = code_words
        return possible_responses


class PotentialOutcomes(dict):
    def __init__(self, data={}):
        self._code_words = set()
        super().__init__(self)
        for guess, responses in data.items():
            for response, code_words in responses.items():
                [self.add(guess, response, w) for w in code_words]

    def add(self, guess, response, code_word):
        if self.get(guess) is None:
            self[guess] = PossibleResponses(guess)
        self[guess][response].add(code_word)
        self._code_words.add(code_word)

    def get_by_guess_response(self, guess, response):
        return self[guess][response]

    @property
    def guesses(self):
        return set(self.keys())

    @property
    def total_length(self):
        return len(self._code_words)

    @property
    def all_code_words(self):
        return self._code_words


def get_potentials(remaining_code_words, get_response, game_log):
    remaining_code_words = set(remaining_code_words)
    indexed_potentials = PotentialOutcomes()
    potential_guesses = 'esiarntolcdupmghbyfvkwzxqj'
    worthwhile_guesses = set(''.join(remaining_code_words))
    for code_word in remaining_code_words:
        for guess in set(code_word):
            response = get_response(code_word, guess)
            indexed_potentials.add(guess, response, code_word)
    for guess, possible_responses in indexed_potentials.items():
        seen_words = set()
        for response, words in possible_responses.items():
            seen_words |= words
        non_matches = remaining_code_words - seen_words
        if non_matches != set():
            indexed_potentials[guess]['!'] = non_matches

    return indexed_potentials


        # (hangman) Chriss-iMac:hangman chris$ time PYTHONPATH=`pwd` cat build/splits/9 | python -m cProfile -s time hang/play.py - --limit 50
# 25011
# Average guesses:  6.16
#          260180638 function calls (260180405 primitive calls) in 162.902 seconds
#
#    Ordered by: internal time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#  36838030   37.044    0.000   55.060    0.000 player.py:178(add)
#    249848   33.010    0.000   33.010    0.000 {method 'ln' of 'decimal.Decimal' objects}
#       308   22.951    0.075  122.328    0.397 player.py:200(get_potentials)
#  36838338   21.084    0.000   44.287    0.000 opponent.py:8(get_response)
#  73677529   19.944    0.000   19.944    0.000 {method 'get' of 'dict' objects}
#  73676517   12.980    0.000   12.980    0.000 {method 'add' of 'set' objects}
#  37489836    7.588    0.000    7.588    0.000 {method 'join' of 'str' objects}
#      5860    2.005    0.000    2.480    0.000 player.py:15(_get_pmf_for_success)
#       308    1.561    0.005   39.561    0.128 player.py:40(_get_counts)
#      5860    1.252    0.000    1.769    0.000 player.py:30(_get_pmf_for_entropy)
#        50    0.916    0.018  162.851    3.257 play.py:10(play)
#    249848    0.719    0.000    0.719    0.000 {method 'isdisjoint' of 'set' objects}
#    650286    0.715    0.000    0.715    0.000 opponent.py:18(<listcomp>)
#    124924    0.570    0.000   33.580    0.000 entropy.py:76(log_probability)
#     11720    0.133    0.000    0.171    0.000 entropy.py:15(get_pmf)
#     23441    0.107    0.000    0.107    0.000 {built-in method builtins.sum}
#     11978    0.062    0.000    0.086    0.000 __init__.py:519(__init__)
#      5860    0.061    0.000   33.642    0.006 entropy.py:28(<listcomp>)
#      5860    0.033    0.000   33.751    0.006 entropy.py:23(get_entropy)
# 161035/161014    0.026    0.000    0.026    0.000 {built-in method builtins.len}
#      5860    0.021    0.000    0.021    0.000 player.py:152(__init__)
#       308    0.019    0.000   39.605    0.129 player.py:76(strategy)
#     11978    0.014    0.000    0.021    0.000 __init__.py:588(update)
#         1    0.011    0.011    0.032    0.032 play.py:43(<listcomp>)
#     25012    0.010    0.000    0.017    0.000 fileinput.py:248(__next__)
#     25012    0.007    0.000    0.007    0.000 {method 'readline' of '_io.TextIOWrapper' objects}

# (hangman) Chriss-iMac:hangman chris$ time PYTHONPATH=`pwd` cat build/splits/9 | python -m cProfile -s time hang/play.py - --limit 50
# 25011
# Average guesses:  6.16
#          223342259 function calls (223342026 primitive calls) in 148.641 seconds
#
#    Ordered by: internal time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#  36838028   36.443    0.000   54.358    0.000 player.py:178(add)
#    249842   32.865    0.000   32.865    0.000 {method 'ln' of 'decimal.Decimal' objects}
#       308   23.288    0.076  108.188    0.351 player.py:200(get_potentials)
#  73677525   21.727    0.000   21.727    0.000 {method 'get' of 'dict' objects}
#  73676512   13.006    0.000   13.006    0.000 {method 'add' of 'set' objects}
#  36838336   12.862    0.000   30.510    0.000 opponent.py:8(get_response)
#      5859    2.029    0.000    2.508    0.000 player.py:15(_get_pmf_for_success)
#       308    1.574    0.005   39.432    0.128 player.py:40(_get_counts)
#      5859    1.243    0.000    1.753    0.000 player.py:30(_get_pmf_for_entropy)
#        50    0.923    0.018  148.589    2.972 play.py:10(play)
#    249842    0.720    0.000    0.720    0.000 {method 'isdisjoint' of 'set' objects}
#    650286    0.700    0.000    0.700    0.000 opponent.py:18(<listcomp>)
#    124921    0.564    0.000   33.428    0.000 entropy.py:76(log_probability)
#    651498    0.140    0.000    0.140    0.000 {method 'join' of 'str' objects}
#     11718    0.131    0.000    0.169    0.000 entropy.py:15(get_pmf)
#     23437    0.106    0.000    0.106    0.000 {built-in method builtins.sum}
#      5859    0.062    0.000   33.490    0.006 entropy.py:28(<listcomp>)
#     11976    0.059    0.000    0.082    0.000 __init__.py:519(__init__)
#      5859    0.032    0.000   33.598    0.006 entropy.py:23(get_entropy)
# 161029/161008    0.026    0.000    0.026    0.000 {built-in method builtins.len}

# ± cc |big-refactor ✗| → time cat build/splits/9 | PYTHONPATH=`pwd` python -m cProfile -s time hang/play.py - --limit 50
# 25011
# Average guesses:  6.16
#          64394561 function calls (64394316 primitive calls) in 83.988 seconds
#
#    Ordered by: internal time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#    249832   38.038    0.000   38.038    0.000 {method 'ln' of 'decimal.Decimal' objects}
#       308   12.316    0.040   35.731    0.116 player.py:200(get_potentials)
#  10505375   11.538    0.000   15.945    0.000 player.py:178(add)
#  21012207    4.186    0.000    4.186    0.000 {method 'get' of 'dict' objects}
#  10505683    4.076    0.000    7.369    0.000 opponent.py:8(get_response)
#  21011201    3.171    0.000    3.171    0.000 {method 'add' of 'set' objects}
#      5856    2.807    0.000    3.470    0.001 player.py:15(_get_pmf_for_success)
#      5856    2.218    0.000    3.000    0.001 player.py:30(_get_pmf_for_entropy)
#       308    1.347    0.004   47.252    0.153 player.py:40(_get_counts)
#    124916    1.190    0.000   39.229    0.000 entropy.py:76(log_probability)
#    249832    1.143    0.000    1.143    0.000 {method 'isdisjoint' of 'set' objects}
#        50    0.862    0.017   83.921    1.678 play.py:10(play)
#    184628    0.284    0.000    0.284    0.000 opponent.py:18(<listcomp>)
#     11712    0.159    0.000    0.206    0.000 entropy.py:15(get_pmf)
#    185849    0.153    0.000    0.153    0.000 {method 'join' of 'str' objects}
#     23425    0.140    0.000    0.140    0.000 {built-in method builtins.sum}
#     11970    0.061    0.000    0.084    0.000 __init__.py:496(__init__)
#      5856    0.061    0.000   39.289    0.007 entropy.py:28(<listcomp>)
#      5856    0.048    0.000   39.435    0.007 entropy.py:23(get_entropy)
#       308    0.048    0.000   47.326    0.154 player.py:76(strategy)
# 161011/160988    0.022    0.000    0.022    0.000 {built-in method builtins.len}
#     25012    0.016    0.000    0.020    0.000 fileinput.py:255(__next__)
#     11970    0.014    0.000    0.020    0.000 __init__.py:565(update)
#         1    0.012    0.012    0.035    0.035 play.py:43(<listcomp>)
#         4    0.006    0.002    0.010    0.003 {built-in method _imp.create_dynamic}
#      5856    0.006    0.000    0.006    0.000 player.py:152(__init__)