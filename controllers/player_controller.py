# controllers/player_controller.py

from models.player import Player
from database import players_table
from views.player_view import PlayerView


class PlayerController:

    def __init__(self):
        self.view = PlayerView()

    def create_player(self):
        data = self.view.ask_player_info()
        player = Player(**data)
        players_table.insert(player.to_dict())
        self.view.confirm_player_created(player)

    def list_players(self):
        records = players_table.all()
        players = [Player.from_dict(r) for r in records]
        self.view.show_players(players)

    def load_players_lookup(self):
        records = players_table.all()
        players = [Player.from_dict(r) for r in records]
        return {p.national_id: p for p in players}
