# controllers/player_controller.py

from models.player import Player
from database import players_table, PlayerQuery
from views.player_view import PlayerView
from rich.console import Console

console = Console()


class PlayerController:
    """
    Contrôleur responsable de :
    - créer un joueur
    - afficher les joueurs
    - supprimer un joueur par numéro
    """

    def __init__(self):
        self.view = PlayerView()

    # --------------------------------------------------------------
    # Création
    # --------------------------------------------------------------
    def create_player(self):
        data = self.view.ask_player_info()
        if data is None:
            return

        player = Player(**data)
        players_table.insert(player.to_dict())
        self.view.confirm_player_created(player)

    # --------------------------------------------------------------
    # Liste
    # --------------------------------------------------------------
    def list_players(self):
        records = players_table.all()
        players = [Player.from_dict(r) for r in records]
        self.view.show_players(players)

    # --------------------------------------------------------------
    # Suppression par numéro
    # --------------------------------------------------------------
    def delete_player(self):
        records = players_table.all()
        players = [Player.from_dict(r) for r in records]

        if not players:
            console.print("[red]Aucun joueur enregistré.[/red]")
            return

        self.view.show_players(players)

        raw = self.view.safe_input("Numéro du joueur à supprimer : ")
        if raw is None:
            return

        try:
            index = int(raw) - 1
            player = players[index]
        except:
            console.print("[red]Numéro invalide.[/red]")
            return

        players_table.remove(PlayerQuery.national_id == player.national_id)
        self.view.confirm_player_deleted(player)
