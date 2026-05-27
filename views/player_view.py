# views/player_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class PlayerView:

    def safe_input(self, message):
        value = console.input(message)
        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée, retour au menu.[/yellow]")
            return None
        return value

    def ask_player_info(self):
        console.print(Panel.fit("[bold cyan]Création d'un joueur[/bold cyan]"))

        last_name = self.safe_input("Nom : ")
        if last_name is None:
            return None

        first_name = self.safe_input("Prénom : ")
        if first_name is None:
            return None

        birthdate = self.safe_input("Date de naissance (JJ/MM/AAAA) : ")
        if birthdate is None:
            return None

        national_id = self.safe_input("Identifiant national : ")
        if national_id is None:
            return None

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
