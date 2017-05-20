def get_response(code_word, guess):
    result = []
    for symbol in code_word:
        if guess == symbol or guess == code_word:
            result.append(symbol)
        else:
            result.append('-')
    if set(result) == {'-'}:
        return '!'
    return ''.join(result)
