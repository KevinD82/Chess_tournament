# controllers/player_controller.py

from models.player import Player
from database import players_table, PlayerQuery
from views.player_view import PlayerView
from rich.console import Console

console = Console()


class PlayerController:

    def __init__(self):
        self.view = PlayerView()

    # --------------------------------------------------------------
    # Récupération de tous les joueurs (objets Player)
    # --------------------------------------------------------------
    def get_all_players(self):
        players = []
        for data in players_table.all():
            players.append(Player.from_dict(data))
        return players

    # --------------------------------------------------------------
    # Création d’un joueur
    # --------------------------------------------------------------
    def create_player(self):
        data = self.view.ask_player_info()
        if not data:
            return

        player = Player(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birthdate=data["birthdate"],
            national_id=data["national_id"],
        )

        players_table.insert(player.to_dict())
        self.view.confirm_player_created(player)

    # --------------------------------------------------------------
    # Liste des joueurs
    # --------------------------------------------------------------
    def list_players(self):
        players = self.get_all_players()
        if not players:
            console.print("[yellow]Aucun joueur enregistré.[/yellow]")
            return

        self.view.show_players(players)

    # --------------------------------------------------------------
    # Suppression d’un joueur
    # --------------------------------------------------------------
    def delete_player(self):
        players = self.get_all_players()
        if not players:
            console.print("[yellow]Aucun joueur à supprimer.[/yellow]")
            return

        self.view.show_players(players)

        choice = console.input("Numéro du joueur à supprimer : ")

        try:
            index = int(choice) - 1
            player = players[index]
        except:
            console.print("[red]Choix invalide.[/red]")
            return

        # Suppression dans TinyDB
        players_table.remove(PlayerQuery.national_id == player.national_id)

        self.view.confirm_player_deleted(player)
