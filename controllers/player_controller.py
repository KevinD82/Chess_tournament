# controllers/player_controller.py

from models.player import Player
from database import players_table
from views.player_view import PlayerView
from tinydb import where
from rich.console import Console

console = Console()


class PlayerController:
    def __init__(self):
        self.view = PlayerView()

    # --------------------------------------------------------------
    # Création d’un joueur
    # --------------------------------------------------------------
    def create_player(self):
        data = self.view.ask_player_info()
        if not data:
            return

        player = Player(**data)
        players_table.insert(player.to_dict())

    # --------------------------------------------------------------
    # Affichage des joueurs
    # --------------------------------------------------------------
    def list_players(self):
        players = [Player.from_dict(p) for p in players_table.all()]
        self.view.show_players(players)

    # --------------------------------------------------------------
    # Suppression d’un joueur (simple et robuste)
    # --------------------------------------------------------------
    def delete_player(self):
        players = [Player.from_dict(p) for p in players_table.all()]

        if not players:
            console.print("[yellow]Aucun joueur enregistré.[/yellow]")
            return

        # Afficher la liste avec numéros
        self.view.show_players(players)

        while True:
            choice = console.input("Numéro du joueur à supprimer (Entrée vide = annuler) : ").strip()

            if choice == "":
                console.print("[yellow]Suppression annulée.[/yellow]")
                return

            if not choice.isdigit():
                console.print("[red]Veuillez entrer un numéro valide.[/red]")
                continue

            index = int(choice) - 1

            if index < 0 or index >= len(players):
                console.print("[red]Numéro hors liste.[/red]")
                continue

            player = players[index]
            break

        # Suppression dans TinyDB
        players_table.remove(where("national_id") == player.national_id)

        console.print(f"[green]Joueur {player.first_name} {player.last_name} supprimé.[/green]")
