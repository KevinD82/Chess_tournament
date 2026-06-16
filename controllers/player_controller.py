# controllers/player_controller.py

from datetime import datetime, date
from models.player import Player
from models.tournament import Tournament
from database import players_table, tournaments_table
from views.player_view import PlayerView
from tinydb import where
from rich.console import Console

console = Console()


class PlayerController:
    """Logique métier liée aux joueurs."""

    def __init__(self):
        self.view = PlayerView()

    def create_player(self):
        """Création d'un joueur avec vérification stricte de l'âge >= 10 ans."""
        console.print("\n[bold magenta]=== AJOUT D'UN NOUVEAU JOUEUR ===[/bold magenta]")
        self.list_players()

        data = self.view.ask_player_info()
        if not data:
            return

        # Validation de l'âge (via la date récupérée)
        try:
            birth_date_str = data.get("birth_date") or data.get("birthdate")
            birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date()
            today = date.today()
            age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day)
            )

            if age < 10:
                console.print(f"[bold red]ERREUR : Âge ({age} ans). Minimum 10 ans requis ![/bold red]")
                return
        except ValueError:
            console.print("[bold red]ERREUR : Format de date invalide.[/bold red]")
            return

        if players_table.search(where("national_id") == data["national_id"]):
            console.print(f"\n[bold red]Erreur : L'ID '{data['national_id']}' existe déjà ![/bold red]")
            return

        player = Player(**data)
        players_table.insert(player.to_dict())
        console.print("[green]Joueur créé avec succès ![/green]")

    def list_players(self):
        players = [Player.from_dict(p) for p in players_table.all()]
        self.view.show_players(players)

    def delete_player(self):
        players = [Player.from_dict(p) for p in players_table.all()]
        if not players:
            console.print("[yellow]Aucun joueur enregistré.[/yellow]")
            return

        self.view.show_players(players)
        while True:
            choice = console.input("Numéro du joueur (Entrée = annuler) : ").strip()
            if choice == "":
                return
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(players):
                    player = players[index]
                    break

        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        is_in_ongoing = any(player.national_id in t.players and len(t.rounds) < t.number_of_rounds for t in tournaments)

        if is_in_ongoing:
            console.print("[bold red]Action impossible : Joueur inscrit dans un tournoi en cours.[/bold red]")
            return

        if any(player.national_id in t.players for t in tournaments):
            players_table.update({"is_active": False}, where("national_id") == player.national_id)
            console.print("[green]Joueur passé en statut Inactif.[/green]")
        else:
            players_table.remove(where("national_id") == player.national_id)
            console.print("[green]Joueur supprimé définitivement.[/green]")
