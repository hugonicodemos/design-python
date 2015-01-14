def poker(hands):
    """ Return the best hand: poker([hand,...]) => hand """
    return max(hands, key=hand_rank)

def hand_rank(hand):
    return None

def test():
    """ Test cases for the functions in poker program. """



print max([3, 4, 5, 0]), max([3, 4, -5, 0], key=abs)