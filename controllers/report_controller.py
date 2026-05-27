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

    def tournament_details(self):
        name = self.view.ask_tournament_name()
        record = tournaments_table.get(TournamentQuery.name == name)

        if not record:
            self.view.error_not_found()
            return

        players_lookup = self.player_controller.load_players_lookup()
        tournament = Tournament.from_dict(record, players_lookup)

        self.view.show_tournament_details(tournament)

    def tournament_rounds(self):
        name = self.view.ask_tournament_name()
        record = tournaments_table.get(TournamentQuery.name == name)

        if not record:
            self.view.error_not_found()
            return

        players_lookup = self.player_controller.load_players_lookup()
        tournament = Tournament.from_dict(record, players_lookup)

        self.view.show_rounds(tournament.rounds)

    def tournament_matches(self):
        name = self.view.ask_tournament_name()
        record = tournaments_table.get(TournamentQuery.name == name)

        if not record:
            self.view.error_not_found()
            return

        players_lookup = self.player_controller.load_players_lookup()
        tournament = Tournament.from_dict(record, players_lookup)

        self.view.show_matches(tournament.rounds)

    def tournament_scores(self):
        name = self.view.ask_tournament_name()
        record = tournaments_table.get(TournamentQuery.name == name)

        if not record:
            self.view.error_not_found()
            return

        players_lookup = self.player_controller.load_players_lookup()
        tournament = Tournament.from_dict(record, players_lookup)

        self.view.show_final_scores(tournament.players)

    def full_history(self):
        name = self.view.ask_tournament_name()
        record = tournaments_table.get(TournamentQuery.name == name)

        if not record:
            self.view.error_not_found()
            return

        players_lookup = self.player_controller.load_players_lookup()
        tournament = Tournament.from_dict(record, players_lookup)

        self.view.show_full_history(tournament)
