# views/tournament_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class TournamentView:

    def ask_tournament_info(self):
        console.print(Panel.fit("[bold cyan]Création d'un tournoi[/bold cyan]"))

        name = console.input("Nom du tournoi : ")
        location = console.input("Lieu : ")
        start_date = console.input("Date de début : ")
        end_date = console.input("Date de fin : ")
        description = console.input("Description : ")

        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description
        }

    def select_players(self, players):
        console.print(Panel.fit("[bold cyan]Sélection des joueurs[/bold cyan]"))

        table = Table(title="Joueurs disponibles")
        table.add_column("Index", style="yellow")
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("ID", style="magenta")

        for i, p in enumerate(players):
            table.add_row(str(i), p.last_name, p.first_name, p.national_id)

        console.print(table)

        indexes = console.input("Entrez les index des joueurs (séparés par des virgules) : ")
        indexes = [int(i.strip()) for i in indexes.split(",")]

        return [players[i] for i in indexes]

    def confirm_tournament_created(self, tournament):
        console.print(f"[green]Tournoi '{tournament.name}' créé avec succès ![/green]")

    def show_tournaments(self, tournaments):
        table = Table(title="Tournois enregistrés")

        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="magenta")
        table.add_column("Dates", style="green")

        for t in tournaments:
            dates = f"{t.start_date} → {t.end_date}"
            table.add_row(t.name, t.location, dates)

        console.print(table)

    def ask_tournament_name(self):
        return console.input("Nom du tournoi à gérer : ")

    def error_not_found(self):
        console.print("[red]Tournoi introuvable.[/red]")

    def tournament_menu(self, tournament):
        console.print(Panel.fit(f"[bold cyan]Gestion du tournoi : {tournament.name}[/bold cyan]"))

        console.print("1. Créer un round")
        console.print("2. Saisir les résultats du round")
        console.print("0. Retour\n")

        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    def show_round(self, round_obj):
        console.print(f"[cyan]Nouveau round créé : {round_obj.name}[/cyan]")
