# controllers/report_controller.py

from rich.console import Console
from rich.panel import Panel
from models.tournament import Tournament
from database import tournaments_table

console = Console()


class ReportController:

    # --------------------------------------------------------------
    # Liste des tournois
    # --------------------------------------------------------------
    def list_tournaments(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        console.print(Panel.fit("[bold cyan]Liste des tournois[/bold cyan]\n"))

        for i, t in enumerate(tournaments, start=1):
            console.print(f"{i}. {t.name} ({t.location}) — {t.start_date} → {t.end_date}")

    # --------------------------------------------------------------
    # Détails d’un tournoi
    # --------------------------------------------------------------
    def tournament_details(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        # Sélection sécurisée du tournoi
        while True:
            choice = console.input("Numéro du tournoi : ").strip()

            if not choice.isdigit():
                console.print("[red]Veuillez entrer un numéro valide.[/red]")
                continue

            index = int(choice) - 1

            if index < 0 or index >= len(tournaments):
                console.print("[red]Numéro hors liste.[/red]")
                continue

            tournament = tournaments[index]
            break

        # Affichage des infos générales
        console.print(Panel.fit(
            f"[bold cyan]{tournament.name}[/bold cyan]\n"
            f"Lieu : {tournament.location}\n"
            f"Dates : {tournament.start_date} → {tournament.end_date}\n"
            f"Description : {tournament.description}\n"
        ))

        # Aucun round enregistré
        if not tournament.rounds:
            console.print("[yellow]Aucun round enregistré pour ce tournoi.[/yellow]")
            return

        # ----------------------------------------------------------
        # AFFICHAGE DES ROUNDS
        # ----------------------------------------------------------
        for i, round_data in enumerate(tournament.rounds, start=1):
            console.print(f"\n[bold yellow]Round {i}[/bold yellow]")

            if not round_data:
                console.print("[red]Round vide.[/red]")
                continue

            for match in round_data:
                console.print(
                    f"{match['p1']} ({match['s1']}) vs {match['p2']} ({match['s2']})"
                )

        # ----------------------------------------------------------
        # AFFICHAGE DU CLASSEMENT FINAL
        # ----------------------------------------------------------
        if tournament.results:
            console.print("\n[bold green]=== Classement final ===[/bold green]")
            for pos, (player, score) in enumerate(tournament.results, start=1):
                console.print(f"{pos}. {player} — {score} pts")
