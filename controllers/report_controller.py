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

        while True:
            choice = console.input("Numéro du tournoi : ").strip()

            if not choice.isdigit():
                console.print("[red]Numéro invalide.[/red]")
                continue

            index = int(choice) - 1

            if index < 0 or index >= len(tournaments):
                console.print("[red]Numéro hors liste.[/red]")
                continue

            tournament = tournaments[index]
            break

        console.print(Panel.fit(
            f"[bold cyan]{tournament.name}[/bold cyan]\n"
            f"Lieu : {tournament.location}\n"
            f"Début : {tournament.start_date} {tournament.start_time}\n"
            f"Fin   : {tournament.end_date} {tournament.end_time}\n"
            f"Description : {tournament.description}\n"
        ))

        if not tournament.rounds:
            console.print("[yellow]Aucun round enregistré.[/yellow]")
            return

        for i, round_data in enumerate(tournament.rounds, start=1):
            console.print(f"\n[bold yellow]Round {i}[/bold yellow]")
            for match in round_data:
                console.print(f"{match['p1']} ({match['s1']}) vs {match['p2']} ({match['s2']})")

        if tournament.results:
            console.print("\n[bold green]=== Classement final ===[/bold green]")
            for pos, (player, score) in enumerate(tournament.results, start=1):
                console.print(f"{pos}. {player} — {score} pts")

    def full_history(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        console.print(Panel.fit("[bold cyan]Historique complet des tournois[/bold cyan]\n"))

        for i, t in enumerate(tournaments, start=1):
            console.print(
                f"{i}. [bold]{t.name}[/bold] — {t.location}\n"
                f"   Début : {t.start_date} {t.start_time}\n"
                f"   Fin   : {t.end_date} {t.end_time}\n"
            )

            if t.results:
                console.print("   [bold green]Classement final :[/bold green]")
                for pos, (player, score) in enumerate(t.results, start=1):
                    console.print(f"      {pos}. {player} — {score} pts")
            else:
                console.print("   [yellow]Aucun classement enregistré.[/yellow]")

            console.print()
