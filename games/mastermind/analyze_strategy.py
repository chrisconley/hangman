from games.mastermind import opponent


def play(code_word, strategy, index, response_sentinel):
    guesses = []
    strategy_place = strategy['']
    while True:
        if type(strategy_place) == int and strategy_place == 1:
            # For compact representations where they don't give us the final correct code word
            # add a response for correct counting purposes
            guesses.append('gotit')
            break

        if strategy_place[1] < 'A':
            guess = strategy_place[1]
        else:
            strategy_place = strategy[strategy_place[1]]
            guess = strategy_place[1]
        response = opponent.get_response(code_word, guess)

        if type(strategy_place) == list and len(strategy_place) == 2:
            # For compact representations where they don't give us the final correct code word
            # add a response for this turn and the final turn for correct counting purposes
            # Ex: [4, '3456']
            guesses.append('gotit')
            if response != response_sentinel:
                guesses.append('gotit')
            break

        strategy_place = strategy_place[2][index[response]]
        guesses.append(guess)
        if response == response_sentinel:
            assert guess == code_word
            break
    return guesses


def analyze(words, strategy, index, response_sentinel):
    total_guesses = 0
    for word in words:
        guesses = play(word, strategy, index, response_sentinel)
        total_guesses += len(guesses)

    return {
        'total_guesses': total_guesses
    }