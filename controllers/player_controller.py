# controllers/player_controller.py

from models.player import Player
from database import players_table
from views.player_view import PlayerView
from tinydb import where
from rich.console import Console

console = Console()


class PlayerController:
    def __init__(self):
        """Initialise le contrôleur des joueurs avec sa vue dédiée."""
        self.view = PlayerView()

    def create_player(self):
        """Gère le formulaire de création d'un joueur et l'enregistre en base."""
        data = self.view.ask_player_info()
        if not data:
            return

        player = Player(**data)
        players_table.insert(player.to_dict())
        console.print("[green]Joueur créé avec succès ![/green]")

    def list_players(self):
        """Récupère et affiche la liste de tous les joueurs enregistrés."""
        players = [Player.from_dict(p) for p in players_table.all()]
        self.view.show_players(players)

    def delete_player(self):
        """Permet de sélectionner et de supprimer un joueur de la base de données."""
        players = [Player.from_dict(p) for p in players_table.all()]

        if not players:
            console.print("[yellow]Aucun joueur enregistré.[/yellow]")
            return

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
        console.print(f"[green]Joueur {player.first_name} {player.last_name} supprimé avec succès ![/green]")
