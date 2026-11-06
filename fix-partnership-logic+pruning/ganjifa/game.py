import json
import os

try:
    from .deck import Deck
    from .trick import Trick
except ImportError:  # pragma: no cover - supports script execution
    from deck import Deck
    from trick import Trick


class Game:
    def __init__(self, players, partnerships=None):
        self.players = players
        self.partnerships = partnerships or []
        self.deck = Deck()
        self.tricks = []

    def setup(self):
        for player in self.players:
            player.hand = []
            player.tricks = []
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.deal(self.players)

    def play_trick(self):
        trick = Trick()
        for index, player in enumerate(self.players):
            card = player.choose_card(self, trick, index)
            if card is None:
                continue
            trick.play(player, card)
        winner = trick.winner()
        winner.tricks.append(trick)
        self.tricks.append({
            "winner": winner.name,
            "cards": trick.to_dict(),
        })
        print(f"{winner.name} won the trick with {trick.to_dict()}")
        return winner

    def play_all_tricks(self, output_path=None):
        results = {player.name: 0 for player in self.players}
        self.tricks = []
        while self.players and self.players[0].hand:
            winner = self.play_trick()
            results[winner.name] += 1

        summary = {
            "results": results,
            "overall_winner": self._overall_winner(results),
            "tricks": self.tricks,
        }
        if output_path is not None:
            directory = os.path.dirname(output_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as handle:
                json.dump(summary, handle, indent=2)
        return summary

    def _team_member_names(self, team):
        names = []
        for member in team:
            if hasattr(member, "name"):
                names.append(member.name)
            elif member is not None:
                names.append(member)
        return tuple(names)

    def _overall_winner(self, results):
        if self.partnerships:
            team_scores = {}
            for team in self.partnerships:
                team_names = self._team_member_names(team)
                team_score = sum(results.get(name, 0) for name in team_names)
                team_scores[team_names] = team_score
            winning_team = max(team_scores, key=team_scores.get)
            return list(winning_team)
        return max(results, key=results.get)
