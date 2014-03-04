def build_power_scorer(known_power=1.0, missed_power=1.0):
    """
    known_letters and missed_letters can either be the number or probability of each
    """
    def power_scorer(known_letters, missed_letters):
        return float(known_letters**known_power) + float(missed_letters**missed_power)

    return power_scorer

def build_multiplier_scorer(known_multiplier=1.0, missed_multiplier=1.0):
    """
    known_letters and missed_letters can either be the number or probability of each
    """
    def multiplier_scorer(known_letters, missed_letters):
        return float(known_letters*known_multiplier) + float(missed_letters*missed_multiplier)

    return multiplier_scorer
