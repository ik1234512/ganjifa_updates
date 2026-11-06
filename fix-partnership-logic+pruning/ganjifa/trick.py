try:
    from .rules import beats
except ImportError:  # pragma: no cover - supports script execution
    from rules import beats


class Trick:
    def __init__(self):
        self.cards = []

    def play(self, player, card):
        if card is None:
            return
        player.remove_card(card)
        self.cards.append((player, card))

    def winner(self):
        lead = self.cards[0][1].suit
        winner = self.cards[0]
        for play in self.cards[1:]:
            if play[1].suit == lead and beats(play[1], winner[1]):
                winner = play
        return winner[0]

    def to_dict(self):
        return [
            {"player": play[0].name, "card": {"suit": play[1].suit.name, "rank": play[1].rank.name}}
            for play in self.cards
        ]
