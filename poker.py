def poker(hands):
    """ Return the best hand: poker([hand,...]) => hand """

    return allmax(hands, key=hand_rank)


def allmax(iterable, key=None):
    """Return a list of all items equal to the max of the iterable."""

    result, max_val = [], None
    key = key or (lambda y: y)

    for x in iterable:
        x_val = key(x)
        if not result or x_val > max_val:
            result, max_val = [x], x_val
        elif x_val == max_val:
            result.append(x)

    return result


def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""

    pair = kind(2, ranks)
    low_pair = kind(2, list(reversed(ranks)))

    if pair and low_pair != pair:
        return pair, low_pair
    else:
        return None


def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-  in the hand."""

    for r in ranks:
        if ranks.count(r) == n:
            return r

    return None


def straight(ranks):
    """Return True if the ordered ranks form a 5-card straight."""

    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5


def flush(hand):
    """Return True if all the cards have the same suit."""

    test_flush = [s for r, s in hand]

    return len(set(test_flush)) == 1


def card_ranks(cards):
    """ Return a list of the ranks, sorted with higher first. """

    ranks = ['--23456789TJQKA'.index(r) for r, s in cards]
    ranks.sort(reverse=True)

    return [5, 4, 3, 2, 1] if ranks == [14, 5, 4, 3, 2] else ranks


def hand_rank(hand):
    """ Return a value indicating the ranking of a hand. """

    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return 8, max(ranks)
    elif kind(4, ranks):
        return 7, kind(4, ranks), kind(1, ranks)
    elif kind(3, ranks) and kind(2, ranks):
        return 6, kind(3, ranks), kind(2, ranks)
    elif flush(hand):
        return 5, ranks
    elif straight(hand):
        return 4, max(ranks)
    elif kind(3, ranks):
        return 3, kind(3, ranks), ranks
    elif two_pair(ranks):
        return 2, two_pair(ranks), ranks
    elif kind(2, ranks):
        return 1, kind(2, ranks), ranks
    else:
        return 0, ranks


def test():
    """ Test cases for the functions in poker program. """

    sf1 = "6C 7C 8C 9C TC".split()  # straight flush
    sf2 = "6C 7C 8C 9C TC".split()  # straight flush
    fk = "9D 9H 9S 9C 7D".split()  # four of a kind
    fh = "TD TC TH 7C 7D".split()  # full house
    tp = "5S 5D 9H 9C 6S".split()  # two pair
    s1 = "AD 2S 3S 4S 5S".split()  # A-5 straight
    s2 = "2C 3C 4D 5S 6S".split()  # 2-6 straight
    ah = "AS 2S 3S 4S 6C".split()  # A high
    sh = "2S 3S 4S 6C 7D".split()  # 7 high

    #assert poker([s1, s2, ah, sh]) == s2
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2]

    fk_ranks = card_ranks(fk)
    tp_ranks = card_ranks(tp)

    assert kind(4, fk_ranks) == 9
    assert kind(3, fk_ranks) is None
    assert kind(2, fk_ranks) is None
    assert kind(1, fk_ranks) == 7
    assert two_pair(fk_ranks) is None
    assert two_pair(tp_ranks) == (9, 5)
    assert straight([9, 8, 7, 6, 5]) is True
    assert straight([9, 8, 8, 6, 5]) is False
    assert flush(sf1) is True
    assert flush(fk) is False
    assert card_ranks(sf1) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]
    assert poker([sf1, fk, fh]) == sf1
    assert poker([fk, fh]) == fk
    assert poker([fh, fh]) == fh
    assert poker([sf1]) == sf1
    assert poker([sf1] + 99*[fh]) == sf1
    assert hand_rank(sf1) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)

    return "tests pass"

print test()

print max([3, 4, 5, 0]), max([3, 4, -5, 0], key=abs)