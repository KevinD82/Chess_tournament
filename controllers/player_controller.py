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
        # Afficher les joueurs existants pour éviter les doublons
        existing_players = [Player.from_dict(p) for p in players_table.all()]
        if existing_players:
            console.print("\n[bold cyan]Joueurs existants :[/bold cyan]")
            self.view.show_players(existing_players)

        data = self.view.ask_player_info()
        if not data:
            return

        # Vérification doublon par national_id
        for p in existing_players:
            if p.national_id == data["national_id"]:
                console.print("[red]Un joueur avec ce National ID existe déjà ![/red]")
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

        # Vérifier si le joueur participe à un tournoi
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        for t in tournaments:
            if player.national_id in getattr(t, "players", []):
                console.print("[red]Impossible de supprimer ce joueur : il participe à un tournoi.[/red]")
                console.print(f"[yellow]Tournoi concerné : {t.name}[/yellow]")
                return

        players_table.remove(where("national_id") == player.national_id)
        console.print(f"[green]Joueur {player.first_name} {player.last_name} supprimé avec succès ![/green]")
