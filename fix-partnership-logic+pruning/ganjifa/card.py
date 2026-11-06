from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    CROWNS = 0
    GOLD = 1
    SWORDS = 2
    SERVANTS = 3
    HARPS = 4
    BILLS = 5
    COINS = 6
    CUPS = 7


class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    MINISTER = 11
    KING = 12


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank

    def __repr__(self):
        return f"Card({self.suit.name}, {self.rank.name})"
