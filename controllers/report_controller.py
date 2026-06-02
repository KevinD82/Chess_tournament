# controllers/report_controller.py

from rich.console import Console
from rich.panel import Panel
from models.player import Player
from models.tournament import Tournament
from database import tournaments_table, players_table  # ✅ TournamentQuery supprimé (inutilisé)

console = Console()


class ReportController:
    def __init__(self):
        pass

    def run(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        console.print(Panel.fit(
            "[bold cyan]=== RAPPORTS ===[/bold cyan]\n\n"
            "1. Liste des tournois\n"
            "2. Détails d’un tournoi\n"
            "0. Retour"
        ))

        choice = console.input("Votre choix : ")

        if choice == "1":
            self.list_tournaments(tournaments)
        elif choice == "2":
            self.tournament_details(tournaments)
        elif choice == "0":
            return
        else:
            console.print("[red]Choix invalide.[/red]")

    # --------------------------------------------------------------
    # Liste des tournois
    # --------------------------------------------------------------
    def list_tournaments(self, tournaments):
        console.print("[bold cyan]Liste des tournois[/bold cyan]\n")
        for i, t in enumerate(tournaments, start=1):
            console.print(f"{i}. {t.name} ({t.location}) — {t.start_date} → {t.end_date}")

    # --------------------------------------------------------------
    # Détails d’un tournoi
    # --------------------------------------------------------------
    def tournament_details(self, tournaments):
        choice = console.input("Numéro du tournoi : ")

        try:
            tournament = tournaments[int(choice) - 1]
        except (ValueError, IndexError) as e:  # ✅ except corrigé
            console.print(f"[red]Choix invalide : {e}[/red]")
            return

        # Recharger les joueurs
        all_players = [Player.from_dict(p) for p in players_table.all()]
        lookup = {p.national_id: p for p in all_players}

        console.print(Panel.fit(
            f"[bold cyan]{tournament.name}[/bold cyan]\n"
            f"Lieu : {tournament.location}\n"
            f"Dates : {tournament.start_date} → {tournament.end_date}\n"
            f"Description : {tournament.description}\n"
        ))

        if not tournament.rounds:
            console.print("[yellow]Aucun round enregistré pour ce tournoi.[/yellow]")
            return

        for r in tournament.rounds:
            console.print(f"\n[bold]Round : {r.name}[/bold]")
            for m in r.matches:
                p1 = lookup.get(m.player1)
                p2 = lookup.get(m.player2)
                if p1 and p2:
                    console.print(
                        f"{p1.first_name} {p1.last_name} ({m.score1}) vs "
                        f"{p2.first_name} {p2.last_name} ({m.score2})"
                    )
