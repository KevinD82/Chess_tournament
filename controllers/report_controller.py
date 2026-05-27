# controllers/report_controller.py

from database import players_table, tournaments_table, TournamentQuery
from models.player import Player
from models.tournament import Tournament
from views.report_view import ReportView
from controllers.player_controller import PlayerController


class ReportController:

    def __init__(self):
        self.view = ReportView()
        self.player_controller = PlayerController()

    def list_all_players(self):
        records = players_table.all()
        players = [Player.from_dict(r) for r in records]
        self.view.show_players(players)

    def list_all_tournaments(self):
        records = tournaments_table.all()
        players_lookup = self.player_controller.load_players_lookup()
        tournaments = [
            Tournament.from_dict(r, players_lookup)
            for r in records
        ]
        self.view.show_tournaments(tournaments)

    def _load_tournament(self):
        name = self.view.ask_tournament_name()
        if name is None:
            return None

        record = tournaments_table.get(TournamentQuery.name == name)
        if not record:
            self.view.error_not_found()
            return None

        players_lookup = self.player_controller.load_players_lookup()
        return Tournament.from_dict(record, players_lookup)

    def tournament_details(self):
        t = self._load_tournament()
        if t:
            self.view.show_tournament_details(t)

    def tournament_rounds(self):
        t = self._load_tournament()
        if t:
            self.view.show_rounds(t.rounds)

    def tournament_matches(self):
        t = self._load_tournament()
        if t:
            self.view.show_matches(t.rounds)

    def tournament_scores(self):
        t = self._load_tournament()
        if t:
            self.view.show_final_scores(t.players)

    def full_history(self):
        t = self._load_tournament()
        if t:
            self.view.show_full_history(t)
