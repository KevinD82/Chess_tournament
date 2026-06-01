# controllers/report_controller.py

from models.player import Player
from models.tournament import Tournament
from database import players_table, tournaments_table
from rich.console import Console

console = Console()


class ReportController:
    """
    Contrôleur responsable de tous les rapports :
    - joueurs
    - tournois
    - rounds
    - matchs
    - scores
    """

    # --------------------------------------------------------------
    # Liste de tous les joueurs
    # --------------------------------------------------------------
    def list_all_players(self):
        players = [Player.from_dict(r) for r in players_table.all()]

        if not players:
            console.print("[red]Aucun joueur enregistré.[/red]")
            return

        console.print("[bold cyan]Liste des joueurs[/bold cyan]")
        for p in players:
            console.print(f"- {p.last_name} {p.first_name} ({p.national_id})")

    # --------------------------------------------------------------
    # Liste de tous les tournois
    # --------------------------------------------------------------
    def list_all_tournaments(self):
        tournaments = [Tournament.from_dict(r) for r in tournaments_table.all()]

        if not tournaments:
            console.print("[red]Aucun tournoi enregistré.[/red]")
            return

        console.print("[bold cyan]Liste des tournois[/bold cyan]")
        for t in tournaments:
            console.print(f"- {t.name} ({t.location})")

    # --------------------------------------------------------------
    # Détails d’un tournoi
    # --------------------------------------------------------------
    def tournament_details(self):
        tournaments = [Tournament.from_dict(r) for r in tournaments_table.all()]

        if not tournaments:
            console.print("[red]Aucun tournoi disponible.[/red]")
            return

        for i, t in enumerate(tournaments, start=1):
            console.print(f"{i}. {t.name}")

        raw = console.input("Numéro du tournoi : ")
        try:
            t = tournaments[int(raw) - 1]
        except:
            console.print("[red]Numéro invalide.[/red]")
            return

        console.print(f"[cyan]{t.name}[/cyan]")
        console.print(f"Lieu : {t.location}")
        console.print(f"Dates : {t.start_date} → {t.end_date}")
        console.print(f"Description : {t.description}")

    # --------------------------------------------------------------
    # Rounds d’un tournoi
    # --------------------------------------------------------------
    def tournament_rounds(self):
        tournaments = [Tournament.from_dict(r) for r in tournaments_table.all()]

        if not tournaments:
            console.print("[red]Aucun tournoi disponible.[/red]")
            return

        for i, t in enumerate(tournaments, start=1):
            console.print(f"{i}. {t.name}")

        raw = console.input("Numéro du tournoi : ")
        try:
            t = tournaments[int(raw) - 1]
        except:
            console.print("[red]Numéro invalide.[/red]")
            return

        if not t.rounds:
            console.print("[yellow]Aucun round enregistré.[/yellow]")
            return

        for r in t.rounds:
            console.print(f"[cyan]{r.name}[/cyan]")

    # --------------------------------------------------------------
    # Matchs d’un tournoi
    # --------------------------------------------------------------
    def tournament_matches(self):
        tournaments = [Tournament.from_dict(r) for r in tournaments_table.all()]

        if not tournaments:
            console.print("[red]Aucun tournoi disponible.[/red]")
            return

        for i, t in enumerate(tournaments, start=1):
            console.print(f"{i}. {t.name}")

        raw = console.input("Numéro du tournoi : ")
        try:
            t = tournaments[int(raw) - 1]
        except:
            console.print("[red]Numéro invalide.[/red]")
            return

        if not t.rounds:
            console.print("[yellow]Aucun match enregistré.[/yellow]")
            return

        for r in t.rounds:
            console.print(f"[cyan]{r.name}[/cyan]")
            for m in r.matches:
                console.print(f"- {m.player1} vs {m.player2}")

    # --------------------------------------------------------------
    # Scores d’un tournoi
    # --------------------------------------------------------------
    def tournament_scores(self):
        tournaments = [Tournament.from_dict(r) for r in tournaments_table.all()]

        if not tournaments:
            console.print("[red]Aucun tournoi disponible.[/red]")
            return

        for i, t in enumerate(tournaments, start=1):
            console.print(f"{i}. {t.name}")

        raw = console.input("Numéro du tournoi : ")
        try:
            t = tournaments[int(raw) - 1]
        except:
            console.print("[red]Numéro invalide.[/red]")
            return

        if not t.rounds:
            console.print("[yellow]Aucun score enregistré.[/yellow]")
            return

        for r in t.rounds:
            console.print(f"[cyan]{r.name}[/cyan]")
            for m in r.matches:
                console.print(f"- {m.player1} {m.score1} vs {m.player2} {m.score2}")

    # --------------------------------------------------------------
    # Historique complet
    # --------------------------------------------------------------
    def full_history(self):
        tournaments = [Tournament.from_dict(r) for r in tournaments_table.all()]

        if not tournaments:
            console.print("[red]Aucun tournoi enregistré.[/red]")
            return

        for t in tournaments:
            console.print(f"\n[bold cyan]{t.name}[/bold cyan]")
            for r in t.rounds:
                console.print(f"  {r.name}")
                for m in r.matches:
                    console.print(f"    - {m.player1} {m.score1} vs {m.player2} {m.score2}")
