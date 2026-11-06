import random

try:
    from .card import Card, Rank, Suit
except ImportError:  # pragma: no cover - supports script execution
    from card import Card, Rank, Suit


class Deck:
    def __init__(self):
        self.cards = [Card(s, r) for s in Suit for r in Rank]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, players):
        while self.cards:
            for player in players:
                if self.cards:
                    player.hand.append(self.cards.pop())
