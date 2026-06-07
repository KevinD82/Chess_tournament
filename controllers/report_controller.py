# controllers/report_controller.py

from rich.console import Console
from rich.panel import Panel
from models.tournament import Tournament
from database import tournaments_table

console = Console()


class ReportController:

    def list_tournaments(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        console.print(Panel.fit("[bold cyan]Liste des tournois[/bold cyan]\n"))

        for i, t in enumerate(tournaments, start=1):
            console.print(f"{i}. {t.name} ({t.location}) — {t.start_date} → {t.end_date}")

    def tournament_details(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        choice = console.input("Numéro du tournoi : ")

        if not choice.isdigit():
            console.print("[red]Choix invalide.[/red]")
            return

        index = int(choice) - 1

        if index < 0 or index >= len(tournaments):
            console.print("[red]Numéro hors liste.[/red]")
            return

        tournament = tournaments[index]

        console.print(Panel.fit(
            f"[bold cyan]{tournament.name}[/bold cyan]\n"
            f"Lieu : {tournament.location}\n"
            f"Dates : {tournament.start_date} → {tournament.end_date}\n"
            f"Description : {tournament.description}\n"
        ))

        if not tournament.rounds:
            console.print("[yellow]Aucun round enregistré pour ce tournoi.[/yellow]")
            return

        for i, rnd in enumerate(tournament.rounds, start=1):
            console.print(f"\n[bold]Round {i}[/bold]")
            for match in rnd:
                console.print(f"{match['p1']} ({match['s1']}) vs {match['p2']} ({match['s2']})")

        if tournament.results:
            console.print("\n[bold green]=== Classement final ===[/bold green]")
            for pos, (player, score) in enumerate(tournament.results, start=1):
                console.print(f"{pos}. {player} — {score} pts")
