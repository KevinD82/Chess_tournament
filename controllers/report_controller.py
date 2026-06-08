# controllers/report_controller.py

from rich.console import Console
from rich.panel import Panel
from models.tournament import Tournament
from models.round import Round
from database import tournaments_table

console = Console()


class ReportController:
    # ------------------------------------------------------------------
    # 1. Affichage de la liste des tournois
    # ------------------------------------------------------------------
    def list_tournaments(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        console.print(Panel.fit("[bold cyan]Liste des tournois[/bold cyan]\n"))

        for i, t in enumerate(tournaments, start=1):
            console.print(f"{i}. {t.name} ({t.location}) — {t.start_date} → {t.end_date}")
    # ------------------------------------------------------------------
    # 2. Affichage des détails d’un tournoi
    # ------------------------------------------------------------------

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

        console.print(
            Panel.fit(
                f"[bold cyan]{tournament.name}[/bold cyan]\n"
                f"Lieu : {tournament.location}\n"
                f"Début : {tournament.start_date} {tournament.start_time}\n"
                f"Fin   : {tournament.end_date} {tournament.end_time}\n"
                f"Description : {tournament.description}"
            )
        )

        # Utilisation de l'instanciation en objet Round pour lire les attributs de Match
        for r_dict in tournament.rounds:
            r_obj = Round.from_dict(r_dict)
            console.print(f"\n[bold yellow]=== {r_obj.name} ===[/bold yellow]")
            for match in r_obj.matches:
                console.print(f"   {match.player1} ({match.score1}) vs {match.player2} ({match.score2})")

        if tournament.results:
            console.print("\n[bold green]=== Classement final ===[/bold green]")
            for pos, (player, score) in enumerate(tournament.results, start=1):
                console.print(f"   {pos}. {player} — {score} pts")

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
