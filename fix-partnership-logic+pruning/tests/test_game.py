import json
import os
import sys
import tempfile
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ganjifa.card import Card, Rank, Suit
from ganjifa.player import BotPlayer, Player
from ganjifa.rules import get_legal_moves
from ganjifa.trick import Trick
from ganjifa.game import Game


def test_legal_moves_follow_lead_suit():
    player = Player("A")
    player.hand = [Card(Suit.CROWNS, Rank.ACE), Card(Suit.GOLD, Rank.ACE)]

    trick = Trick()
    trick.cards = [(None, Card(Suit.CROWNS, Rank.TWO))]

    assert get_legal_moves(player, trick) == [Card(Suit.CROWNS, Rank.ACE)]


def test_bot_returns_legal_move():
    bot = BotPlayer("Bot")
    bot.hand = [Card(Suit.GOLD, Rank.ACE), Card(Suit.CROWNS, Rank.FIVE)]

    trick = Trick()
    trick.cards = [(None, Card(Suit.CROWNS, Rank.TWO))]

    move = bot.choose_card(None, trick, 0)
    assert move in bot.hand
    assert move in get_legal_moves(bot, trick)


def test_player_can_select_numbered_card_and_retry_invalid_choice():
    player = Player("A")
    player.hand = [Card(Suit.CROWNS, Rank.ACE), Card(Suit.GOLD, Rank.KING)]

    with patch.object(sys.stdin, "isatty", return_value=True):
        with patch("builtins.input", side_effect=["9", "2"]):
            move = player.choose_card(None, Trick(), 0)

    assert move == Card(Suit.GOLD, Rank.KING)


def test_game_writes_json_summary(tmp_path):
    players = [Player("A"), Player("B"), Player("C"), Player("D")]
    for player, card in zip(players, [
        Card(Suit.CROWNS, Rank.ACE),
        Card(Suit.CROWNS, Rank.TWO),
        Card(Suit.CROWNS, Rank.THREE),
        Card(Suit.CROWNS, Rank.FOUR),
    ]):
        player.hand = [card]

    game = Game(players)
    output_path = tmp_path / "results.json"

    summary = game.play_all_tricks(output_path=str(output_path))

    assert output_path.exists()
    with output_path.open() as handle:
        loaded = json.load(handle)

    assert loaded["overall_winner"] == summary["overall_winner"]
    assert len(loaded["tricks"]) == 1
