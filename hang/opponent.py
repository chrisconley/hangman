def get_response(code_word, guess):
    if code_word == guess:
        return code_word
    result = []
    for symbol in code_word:
        if guess == symbol:
            result.append(symbol)
        else:
            result.append('-')
    if set(result) == {'-'}:
        return '!'
    return ''.join(result)
