# views/player_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class PlayerView:

    def ask_player_info(self):
        console.print(Panel.fit("[bold cyan]Création d'un joueur[/bold cyan]"))

        last_name = console.input("Nom : ")
        first_name = console.input("Prénom : ")
        birthdate = console.input("Date de naissance (JJ/MM/AAAA) : ")
        national_id = console.input("Identifiant national : ")

        return {
            "last_name": last_name,
            "first_name": first_name,
            "birthdate": birthdate,
            "national_id": national_id
        }

    def confirm_player_created(self, player):
        console.print(f"[green]Joueur {player.first_name} {player.last_name} créé avec succès ![/green]")

    def show_players(self, players):
        table = Table(title="Liste des joueurs")

        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("ID National", style="magenta")
        table.add_column("Score", style="green")

        for p in players:
            table.add_row(p.last_name, p.first_name, p.national_id, str(p.score))

        console.print(table)
