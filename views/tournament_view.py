# views/tournament_view.py

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# --------------------------------------------------------------
# Affichage du tournoi, des rounds et des résultats
# --------------------------------------------------------------
class TournamentView:

    def ask_tournament_info(self):
        console.print(Panel.fit("[bold cyan]Création d'un tournoi[/bold cyan]"))

        name = console.input("Nom du tournoi : ")
        location = console.input("Lieu : ")
        start_date = console.input("Date de début (JJ/MM/AAAA) : ")
        end_date = console.input("Date de fin (JJ/MM/AAAA) : ")
        description = console.input("Description : ")

        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
        }
    # --------------------------------------------------------------
    # Affichage du tournoi
    # --------------------------------------------------------------
    def show_tournaments(self, tournaments):
        table = Table(title="Liste des tournois")

        table.add_column("N°", style="yellow")
        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="cyan")
        table.add_column("Début", style="magenta")
        table.add_column("Fin", style="magenta")

        for i, t in enumerate(tournaments, start=1):
            start = f"{t.start_date} {t.start_time}".strip()
            end = f"{t.end_date} {t.end_time}".strip()
            table.add_row(str(i), t.name, t.location, start, end)

        console.print(table)

    # --------------------------------------------------------------
    # Affichage du round et des matchs
    # --------------------------------------------------------------
    def show_round(self, round_number, matches):
        # Affichage propre utilisant les attributs d'objet Match
        console.print(Panel.fit(f"[bold cyan]Génération des matchs — Round {round_number}[/bold cyan]"))
        for m in matches:
            console.print(f"   [white]{m.player1}[/white] vs [white]{m.player2}[/white]")
        console.print("")

    # --------------------------------------------------------------
    # Affichage des résultats
    # --------------------------------------------------------------
    def show_results(self, results):
        table = Table(title="🏆 CLASSEMENT FINAL DU TOURNOI 🏆")

        table.add_column("Rang", style="yellow", justify="center")
        table.add_column("Joueur", style="cyan")
        table.add_column("Score Total", style="green", justify="center")

        for pos, (player, score) in enumerate(results, start=1):
            table.add_row(str(pos), player, f"{score} pts")

        console.print("\n", table, "\n")
