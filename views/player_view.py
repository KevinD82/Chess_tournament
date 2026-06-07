# views/player_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class PlayerView:
    """
    Vue dédiée à la création et l'affichage des joueurs.
    """

    # --------------------------------------------------------------
    # Création simple d’un joueur
    # --------------------------------------------------------------
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
            "national_id": national_id,
        }

    # --------------------------------------------------------------
    # Affichage des joueurs avec numéro
    # --------------------------------------------------------------
    def show_players(self, players):
        table = Table(title="Liste des joueurs")

        table.add_column("N°", style="yellow")
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("Date de naissance", style="magenta")
        table.add_column("ID", style="yellow")

        for i, p in enumerate(players, start=1):
            table.add_row(
                str(i),
                p.last_name,
                p.first_name,
                p.birthdate,
                p.national_id
            )

        console.print(table)
