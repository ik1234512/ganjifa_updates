try:
    from .card import *
except ImportError:  # pragma: no cover - supports script execution
    from card import *

STRONG = {Suit.CROWNS, Suit.GOLD, Suit.SWORDS, Suit.SERVANTS}
SO = [
    Rank.ACE,
    Rank.TWO,
    Rank.THREE,
    Rank.FOUR,
    Rank.FIVE,
    Rank.SIX,
    Rank.SEVEN,
    Rank.EIGHT,
    Rank.NINE,
    Rank.TEN,
    Rank.MINISTER,
    Rank.KING,
]
WO = list(reversed(SO))


def value(c):
    return (SO if c.suit in STRONG else WO).index(c.rank)


def beats(a, b):
    return a.suit == b.suit and value(a) > value(b)


def get_legal_moves(player, trick):
    return get_legal_moves_from_hand(player.hand, trick)


def get_legal_moves_from_hand(hand, trick):
    if not hand:
        return []
    if not trick.cards:
        return list(hand)
    lead_suit = trick.cards[0][1].suit
    if any(card.suit == lead_suit for card in hand):
        return [card for card in hand if card.suit == lead_suit]
    return list(hand)
