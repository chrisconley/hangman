def get_response(actual_word, word_guess):
    actual_letters = list(actual_word)
    guess_letters = list(word_guess)
    response = []
    for index, letter in enumerate(guess_letters):
        if letter == actual_word[index]:
            response.append('B')
            actual_letters[index] = '-'
            guess_letters[index] = '-'
    for index, letter in enumerate(guess_letters):
        if letter == '-':
            continue
        if letter in actual_letters:
            response.append('W')
    response_key = ''.join(sorted(response))
    return response_key
