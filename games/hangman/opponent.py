from collections import Counter, OrderedDict

from games import code_words


class OrderedCounter(Counter, OrderedDict):
    pass


class GameLog(list):
    @property
    def guesses(self):
        return {t['guess'] for t in self}

    def get_cache_key(self):
        hidden_word = []
        missed_guesses = set()
        for entry in self:
            if entry['result'] == '!':
                missed_guesses.add(entry['guess'])
            else:
                if hidden_word == []:
                    hidden_word = list(entry['result'])
                else:
                    for index, character in enumerate(entry['result']):
                        if character == '-':
                            continue
                        hidden_word[index] = character
        key = "{}:{}".format("".join(hidden_word), "".join(sorted(missed_guesses)))
        return key

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


def get_potentials(remaining_code_words, get_response, game_log):
    remaining_code_words = set(remaining_code_words)
    indexed_potentials = code_words.PotentialOutcomes()
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
