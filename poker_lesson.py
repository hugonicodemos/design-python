import random


def poker(hands):
    """ Return the best hand: poker([hand, ...]) => [hand, ...] """

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

    for rank in ranks:
        if ranks.count(rank) == n:
            return rank

    return None


def straight(ranks):
    """Return True if the ordered ranks form a 5-card straight."""

    return ((max(ranks) - min(ranks)) == 4) and len(set(ranks)) == 5


def flush(hand):
    """Return True if all the cards have the same suit."""

    test_flush = [suit for rank, suit in hand]

    return len(set(test_flush)) == 1


def card_ranks(cards):
    """ Return a list of the ranks, sorted with higher first. """

    ranks = ['--23456789TJQKA'.index(rank) for rank, suit in cards]
    ranks.sort(reverse=True)

    return [5, 4, 3, 2, 1] if ranks == [14, 5, 4, 3, 2] else ranks


def old_hand_rank(hand):
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
    elif straight(ranks):
        return 4, max(ranks)
    elif kind(3, ranks):
        return 3, kind(3, ranks), ranks
    elif two_pair(ranks):
        return 2, two_pair(ranks), ranks
    elif kind(2, ranks):
        return 1, kind(2, ranks), ranks
    else:
        return 0, ranks


def hand_rank(hand):
    """ Return a value indicating how high the hand ranks. """
    # Count is the count of each rank; ranks lists correspoding ranks
    # E.g '7 T 7 9 7' => counts = (3, 1, 1); ranks = (7, 10, 9)
    groups = group(['--23456789TJQKA'.index(rank) for rank, suit in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
    flush = len(set([suit for rank, suit in hand])) == 1
    return max(count_rankings[counts], 4*straight + 5*flush), ranks


count_rankings = {(5,): 10, (4, 1): 7, (3, 2): 6, (3, 1, 1): 3,
                  (2, 2, 1): 2, (2, 1, 1, 1): 1, (1, 1, 1, 1, 1): 0}


def group(items):
    """ Return a list of [(count, x)...], highest count first, the highest x first. """

    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)


def unzip(pairs):
    return zip(*pairs)


def deal(num_hands, n=5, deck=[r+s for r in '23456789TJKA' for s in 'SHDC']):
    """ Shuffle the deck and deal out num_hands n-cards hands. """

    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(num_hands)]


def hand_percentages(n=700*1000):
    """ Sample n random hands and print a table of percentages for each type of hand. """

    hand_names = ["High Card", "Pair", "2 Pair",
                  "3 Kind", "Straight", "Flush",
                  "Full House", "4 kind", "Straight Flush"]
    counts = [0] * 9
    for i in range(n/10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print "%14s: %6.3f %%" % (hand_names[i], 100.*counts[i]/n)


def test():
    """ Test cases for the functions in poker program. """

    sf1 = "6C 7C 8C 9C TC".split()  # straight flush
    sf2 = "6C 7C 8C 9C TC".split()  # straight flush
    fk = "9D 9H 9S 9C 7D".split()  # four of a kind
    fh = "TD TC TH 7C 7D".split()  # full house
    tp = "5S 5D 9H 9C 6S".split()  # two pair
    s1 = "AD 2S 3S 4S 5S".split()  # A-5 straight
    s2 = "2C 3C 4H 5S 6S".split()  # 2-6 straight
    ah = "AS 2S 3S 4S 6C".split()  # A high
    sh = "2S 3S 4S 6C 7D".split()  # 7 high

    assert poker([s1, s2, ah, sh]) == [s2]
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
    assert poker([sf1, fk, fh]) == [sf1]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf1]) == [sf1]
    assert poker([sf1] + 99*[fh]) == [sf1]
    assert hand_rank(sf1) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)

    return "tests pass"

print test()
#hand_percentages()

print max([3, 4, 5, 0]), max([3, 4, -5, 0], key=abs)
