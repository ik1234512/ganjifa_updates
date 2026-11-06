try:
    from .player import BotPlayer, Player
    from .game import Game
except ImportError:  # pragma: no cover - supports script execution
    from player import BotPlayer, Player
    from game import Game

ps = [Player("A"), BotPlayer("B"), Player("C"), BotPlayer("D")]
g = Game(ps, partnerships=[("A", "C"), ("B", "D")])
g.setup()
summary = g.play_all_tricks(output_path="results.json")

for player in ps:
    print(f"{player.name} won {summary['results'][player.name]} tricks")

print(f"Overall winner: {summary['overall_winner']}")
