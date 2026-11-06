import sys

try:
    from .rules import beats, get_legal_moves
except ImportError:  # pragma: no cover - supports script execution
    from rules import beats, get_legal_moves


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.tricks = []

    def remove_card(self, card):
        self.hand.remove(card)

    def choose_card(self, game, trick, position):
        legal_moves = get_legal_moves(self, trick)
        if not legal_moves:
            return None
        if hasattr(sys.stdin, "isatty") and sys.stdin.isatty():
            print(f"{self.name}, choose a card:")
            for index, card in enumerate(legal_moves, start=1):
                print(f"{index}. {card.rank.name} of {card.suit.name}")
            while True:
                choice = input("card> ").strip()
                if choice.isdigit():
                    card_index = int(choice) - 1
                    if 0 <= card_index < len(legal_moves):
                        return legal_moves[card_index]
                else:
                    for card in legal_moves:
                        if str(card).lower() == choice.lower():
                            return card
                print("Invalid choice, try again.")
        return legal_moves[0]


class BotPlayer(Player):
    def __init__(self, name, lookahead=2):
        super().__init__(name)
        self.lookahead = lookahead

    def choose_card(self, game, trick, position):
        legal_moves = get_legal_moves(self, trick)
        if not legal_moves:
            return None
        if game is None:
            return max(legal_moves, key=self._card_value)

        best_card = legal_moves[0]
        best_score = -float("inf")
        for card in legal_moves:
            score = self._evaluate_move(game, trick, position, card)
            if score > best_score:
                best_score = score
                best_card = card
        return best_card

    def _card_value(self, card):
        return (card.rank.value * 10) + card.suit.value

    def _evaluate_move(self, game, trick, position, card):
        if not game:
            return self._card_value(card)

        turn_order = game.players
        trick_cards = list(trick.cards)
        trick_cards.append((self, card))

        if len(trick_cards) == len(turn_order):
            winner = TrickForSearch(trick_cards, turn_order).winner_index()
            return 1000 if winner == position else -1000

        next_player_index = (position + 1) % len(turn_order)
        next_player = turn_order[next_player_index]
        legal_moves = get_legal_moves(next_player, type("T", (), {"cards": trick_cards})())
        if not legal_moves:
            return 0

        best_score = -float("inf") if next_player is self else float("inf")
        for candidate in legal_moves:
            score = self._evaluate_follow_up(game, turn_order, trick_cards, next_player_index, candidate)
            if next_player is self:
                best_score = max(best_score, score)
            else:
                best_score = min(best_score, score)
        return best_score

    def _evaluate_follow_up(self, game, players, trick_cards, position, card):
        next_trick = list(trick_cards)
        next_trick.append((players[position], card))
        if len(next_trick) == len(players):
            winner = TrickForSearch(next_trick, players).winner_index()
            return 1000 if winner == 0 else -1000
        next_position = (position + 1) % len(players)
        next_player = players[next_position]
        legal_moves = get_legal_moves(next_player, type("T", (), {"cards": next_trick})())
        if not legal_moves:
            return 0
        best_score = -float("inf") if next_player is self else float("inf")
        for candidate in legal_moves:
            score = self._evaluate_follow_up(game, players, next_trick, next_position, candidate)
            if next_player is self:
                best_score = max(best_score, score)
            else:
                best_score = min(best_score, score)
        return best_score


class TrickForSearch:
    def __init__(self, cards, players):
        self.cards = cards
        self.players = players

    def winner_index(self):
        lead_suit = self.cards[0][1].suit
        winner = self.cards[0]
        for play in self.cards[1:]:
            if play[1].suit == lead_suit and beats(play[1], winner[1]):
                winner = play
        return self.cards.index(winner)
