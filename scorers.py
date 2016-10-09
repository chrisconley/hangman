def build_multiplier_scorer(known_multiplier=1.0, missed_multiplier=1.0):
    """
    known_letters and missed_letters can either be the number or probability of each
    """
    def multiplier_scorer(known_letters, missed_letters):
        return (known_letters * known_multiplier) + (missed_letters*missed_multiplier)

    return multiplier_scorer
