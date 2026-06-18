# views/player_view.py

from datetime import datetime
from rich.console import Console
from rich.table import Table
import re

console = Console()


class PlayerView:
    """Affichage et saisie des joueurs."""

    def ask_player_info(self):
        while True:
            console.print("\n[bold cyan]Création d'un joueur[/bold cyan]")
            last_name = console.input("Nom : ").strip()
            if not last_name:
                console.print("[red]Nom vide.[/red]")
                continue
            first_name = console.input("Prénom : ").strip()
            if not first_name:
                console.print("[red]Prénom vide.[/red]")
                continue

            while True:
                birth_date_str = console.input("Date de naissance (JJ/MM/AAAA) : ").strip()
                try:
                    datetime.strptime(birth_date_str, "%d/%m/%Y")
                    break
                except ValueError:
                    console.print("[red]Format invalide (JJ/MM/AAAA).[/red]")

            while True:
                national_id = console.input("ID National (AB12345) : ").strip().upper()
                if re.match(r"^[A-Z]{2}\d{5}$", national_id):
                    break
                console.print("[red]Format invalide.[/red]")

            if console.input("[green]Confirmer ? (O/N) : [/green]").strip().upper() == "O":
                return {
                    "last_name": last_name,
                    "first_name": first_name,
                    "birth_date": birth_date_str,
                    "national_id": national_id
                }

    def show_players(self, players):
        if not players:
            console.print("[yellow]Aucun joueur enregistré.[/yellow]")
            return

        table = Table(show_header=True, header_style="bold cyan", border_style="dim")
        table.add_column("N°", justify="center")
        table.add_column("ID", justify="center")
        table.add_column("Nom")
        table.add_column("Prénom")
        table.add_column("Naissance", justify="center")
        table.add_column("Statut", justify="center")

        for i, p in enumerate(players, 1):
            status = "[green]Actif[/green]" if p.is_active else "[red]Inactif[/red]"
            table.add_row(
                str(i), p.national_id, p.last_name, p.first_name, p.birthdate, status
            )
        console.print(table)
