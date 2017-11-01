from games.mastermind import opponent


def play(code_word, strategy, index, response_sentinel):
    guesses = []
    responses = []
    strategy_place = strategy['']
    while True:
        # For compact representations where they don't give us the final correct code word
        # add a response for correct counting purposes
        if type(strategy_place) == int and strategy_place == 1:
            guesses.append('gotit')
            break

        if type(strategy_place) == int and strategy_place != 1:
            print('----', "I don't think we should be here {}, {}, {}, {}, {}".format(code_word, responses, opponent.get_response(code_word, guess), guesses, index))
            guesses.append('gotit')
            break

        # If this "guess" is a reference to a sub-tree, then update where
        # we are in the strategy tree.
        guess = strategy_place[1]
        if guess >= 'A':
            strategy_place = strategy[guess]
            guess = strategy_place[1]

        response = opponent.get_response_alternative(code_word, guess)
        responses.append(response)

        # For compact representations where they don't give us the final correct code word
        # add a response for this turn. If the response doesn't match the sentinel, then we'll need
        # an additional guess appended to our list of guesses.
        # Ex: [4, '3456']
        if len(strategy_place) == 2:
            guesses.append('gotit')
            if response != response_sentinel:
                guesses.append('gotit')
            break

        assert len(strategy_place[2]) == 14
        assert strategy_place[0] == sum([c[0] if type(c) == list else c for c in strategy_place[2]])

        # Append the actual guess and exit if we've correctly guessed the codeword.
        guesses.append(guess)
        if response == response_sentinel:
            assert guess == code_word
            break

        # Update our place in the strategy tree for the next while loop iteration
        try:
            strategy_place = strategy_place[2][index[response]]
        except IndexError as e:
            print('!!!!!', guesses, response)

    return guesses


def analyze(words, strategy, index, response_sentinel):
    total_guesses = 0
    for word in words:
        guesses = play(word, strategy, index, response_sentinel)
        total_guesses += len(guesses)

    return {
        'total_guesses': total_guesses
    }