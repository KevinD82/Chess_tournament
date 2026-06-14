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

    def run(self):
        while True:
            choice = self.view.display_report_menu()
            if choice == "1":
                self.tournament_details_report()
            elif choice == "2":
                self.full_tournament_report()
            elif choice == "0":
                break
            else:
                console.print("[red]Choix invalide.[/red]")

    def _select_tournament_with_raw_data(self):
        raw_tournaments = tournaments_table.all()
        if not raw_tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return None, None

        for index, t in enumerate(raw_tournaments, start=1):
            console.print(f"{index}. {t.get('name')} ({t.get('location', '')})")

        choice = console.input("\nSélectionnez le numéro du tournoi : ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(raw_tournaments):
            console.print("[red]Numéro invalide.[/red]")
            return None, None

        raw_data = raw_tournaments[int(choice) - 1]
        tournament_obj = Tournament.from_dict(raw_data)
        return tournament_obj, raw_data

    def tournament_details(self):
        self.tournament_details_report()

    def full_history(self):
        self.full_tournament_report()

    def tournament_details_report(self):
        tournament, raw_data = self._select_tournament_with_raw_data()
        if not tournament:
            return

        players_dict = {p['national_id']: Player.from_dict(p) for p in players_table.all()}

        tournament_players = getattr(
            tournament, "players",
            getattr(tournament, "players_list", getattr(tournament, "registered_players", []))
        )

        if not tournament_players and tournament.rounds:
            detected_players = set()
            for round_obj in tournament.rounds:
                if isinstance(round_obj, dict):
                    matches = round_obj.get("matches", [])
                else:
                    matches = getattr(round_obj, "matches", [])

                for match in matches:
                    if isinstance(match, dict):
                        detected_players.add(match.get("player1"))
                        detected_players.add(match.get("player2"))
                    elif hasattr(match, "player1"):
                        detected_players.add(match.player1)
                        detected_players.add(match.player2)
                    else:
                        detected_players.add(match[0][0])
                        detected_players.add(match[1][0])
            tournament_players = list(detected_players)

        tournament.players = tournament_players
        self.view.show_tournament_details(tournament, players_dict)

    def full_tournament_report(self):
        tournament, raw_data = self._select_tournament_with_raw_data()
        if not tournament:
            return

        players_data = {
            p['national_id']: f"{p['last_name']} {p['first_name']}"
            for p in players_table.all()
        }

        raw_rounds = raw_data.get("rounds", [])
        for index, round_obj in enumerate(tournament.rounds):
            if index < len(raw_rounds):
                raw_time = raw_rounds[index].get("start_time", raw_rounds[index].get("date", ""))
                if isinstance(round_obj, dict):
                    round_obj["start_time"] = raw_time
                else:
                    setattr(round_obj, "start_time", raw_time)
                    setattr(round_obj, "date", raw_time)

        scores = {}
        players_list = getattr(tournament, "players", [])
        if not players_list:
            players_list = list(players_data.keys())

        for p_id in players_list:
            scores[p_id] = 0.0

        for round_obj in tournament.rounds:
            if isinstance(round_obj, dict):
                matches = round_obj.get("matches", [])
            else:
                matches = getattr(round_obj, "matches", [])

            for match in matches:
                if isinstance(match, dict):
                    p1, s1 = match.get("player1"), match.get("score1", 0.0)
                    p2, s2 = match.get("player2"), match.get("score2", 0.0)
                elif hasattr(match, "player1"):
                    p1, s1 = match.player1, getattr(match, "score1", 0.0)
                    p2, s2 = match.player2, getattr(match, "score2", 0.0)
                else:
                    p1, s1 = match[0][0], match[0][1]
                    p2, s2 = match[1][0], match[1][1]

                if p1 in scores:
                    scores[p1] += float(s1)
                if p2 in scores:
                    scores[p2] += float(s2)

        ranking = []
        for p_id, score in scores.items():
            player_name = players_data.get(p_id, "Joueur Inconnu")
            ranking.append((p_id, score, player_name))

        ranking.sort(key=lambda x: x[1], reverse=True)
        self.view.show_full_tournament_report(tournament, ranking, players_data)
