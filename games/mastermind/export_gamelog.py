class Leaf(list):
    def __init__(self, index, parent=None):
        self.index = index
        self.parent = parent
        self.append(0)
        self.append('')
        self.append([0] * len(index))

    @property
    def count(self):
        return self[0]

    @count.setter
    def count(self, value):
        self[0] = value

    @property
    def guess(self):
        return self[1]

    @property
    def responses(self):
        if len(self) < 3:
            self.append([0] * len(self.index))
        return self[2]

    @guess.setter
    def guess(self, value):
        self[1] = value

    def init_response(self, guess, response):
        response_index = self.index[response]
        self.responses[response_index] = get_new_leaf(self.index, self)
        self.responses[response_index].guess = guess
        return self.responses[response_index]

    def get_response(self, response):
        response_index = self.index[response]
        return self.responses[response_index]

    def remove_responses(self):
        self.pop()


def get_new_leaf(index, parent=None):
    return Leaf(index, parent)


def update(strategy, log, index):
    if len(log) == 0:
        return strategy

    next_turn = log[0]
    response = next_turn['result']
    guess = next_turn['guess'][0]
    strategy.count += 1
    strategy.guess = guess
    if response == 'BB':
        strategy[2][-1] = 1
        while True:
            if strategy.parent is None:
                return strategy
            else:
                strategy = strategy.parent
    else:
        if strategy.count == 0:
            new_leaf = strategy.init_response(guess, response)
        else:
            new_leaf = strategy.get_response(response)
            if new_leaf == 0:
                new_leaf = strategy.init_response(guess, response)
        return update(new_leaf, log[1:], index)


def export(game_log, index, strategy=None):
    if strategy is None:
        strategy = get_new_leaf(index)
    for game in game_log:
        strategy = update(strategy, game['log'], index)

    return strategy
