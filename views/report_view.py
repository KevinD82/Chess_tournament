# views/report_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class ReportView:

    # Vue dédiée à l'affichage des rapports :
    # - liste des tournois
    # - détails d’un tournoi

    # Cette vue ne contient aucune logique métier.
    # Elle affiche uniquement les données fournies par ReportController.

    # ------------------------------------------------------------------
    # 1. Affichage de la liste des tournois
    # ------------------------------------------------------------------
    def show_tournaments(self, tournaments):
        """
        Affiche tous les tournois enregistrés dans TinyDB.
        """
        table = Table(title="Tournois enregistrés")

        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="magenta")
        table.add_column("Dates", style="green")

        for t in tournaments:
            table.add_row(t.name, t.location, f"{t.start_date} → {t.end_date}")

        console.print(table)

    # ------------------------------------------------------------------
    # 2. Affichage des détails d’un tournoi
    # ------------------------------------------------------------------
    def show_tournament_details(self, tournament):

        # Affiche les informations générales d’un tournoi :
        # - nom
        # - lieu
        # - dates
        # - description

        console.print(
            Panel.fit(
                f"[bold cyan]{tournament.name}[/bold cyan]\n"
                f"Lieu : {tournament.location}\n"
                f"Dates : {tournament.start_date} → {tournament.end_date}\n"
                f"Description : {tournament.description}",
                border_style="cyan"
            )
        )
