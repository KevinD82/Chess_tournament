from models.tournament import Tournament
from models.player import Player
from database import tournaments_table, players_table
from views.report_view import ReportView
from rich.console import Console

console = Console()


class ReportController:
    """Extraction des données et calcul des classements pour les rapports."""

    def __init__(self):
        self.view = ReportView()

    # ---------------------------------------------------------
    # LISTE DES TOURNOIS
    # ---------------------------------------------------------
    def report_tournaments(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        self.view.show_tournament_list(tournaments)

    # ---------------------------------------------------------
    # DÉTAIL D’UN TOURNOI
    # ---------------------------------------------------------
    def report_tournament_details(self):
        raw_tournaments = tournaments_table.all()
        if not raw_tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        for i, t in enumerate(raw_tournaments, 1):
            console.print(f"{i}. {t['name']} ({t['location']})")

        choice = console.input("\nNuméro du tournoi : ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(raw_tournaments):
            console.print("[red]Numéro invalide.[/red]")
            return

        raw = raw_tournaments[int(choice) - 1]
        tournament = Tournament.from_dict(raw)

        players_dict = {p['national_id']: Player.from_dict(p) for p in players_table.all()}

        self.view.show_tournament_details(tournament, players_dict)

    # ---------------------------------------------------------
    # HISTORIQUE COMPLET
    # ---------------------------------------------------------
    def report_full_history(self):
        raw_tournaments = tournaments_table.all()
        if not raw_tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        for i, t in enumerate(raw_tournaments, 1):
            console.print(f"{i}. {t['name']} ({t['location']})")

        choice = console.input("\nNuméro du tournoi : ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(raw_tournaments):
            console.print("[red]Numéro invalide.[/red]")
            return

        raw = raw_tournaments[int(choice) - 1]
        tournament = Tournament.from_dict(raw)

        players_data = {
            p['national_id']: f"{p['last_name']} {p['first_name']}"
            for p in players_table.all()
        }

        # Calcul des scores
        scores = {pid: 0.0 for pid in tournament.players}

        for r in tournament.rounds:
            matches = r.matches if hasattr(r, "matches") else r.get("matches", [])
            for m in matches:
                if isinstance(m, dict):
                    p1, s1 = m["player1"], m["score1"]
                    p2, s2 = m["player2"], m["score2"]
                else:
                    p1, s1 = m.player1, m.score1
                    p2, s2 = m.player2, m.score2

                scores[p1] += float(s1)
                scores[p2] += float(s2)

        ranking = sorted(
            [(pid, score, players_data.get(pid, "Inconnu")) for pid, score in scores.items()],
            key=lambda x: x[1],
            reverse=True
        )

        self.view.show_full_tournament_report(tournament, ranking, players_data)
