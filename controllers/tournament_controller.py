# controllers/tournament_controller.py

from models.tournament import Tournament
from database import tournaments_table, TournamentQuery
from views.tournament_view import TournamentView
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController


class TournamentController:

    def __init__(self):
        self.view = TournamentView()
        self.player_controller = PlayerController()
        self.round_controller = RoundController()

    def create_tournament(self):
        data = self.view.ask_tournament_info()
        if data is None:
            return  # annulé

        players = self.player_controller.load_players_lookup().values()
        selected = self.view.select_players(list(players))
        if selected is None:
            return  # annulé

        tournament = Tournament(**data, players=selected)
        tournaments_table.insert(tournament.to_dict())
        self.view.confirm_tournament_created(tournament)

    def list_tournaments(self):
        records = tournaments_table.all()
        players_lookup = self.player_controller.load_players_lookup()
        tournaments = [
            Tournament.from_dict(r, players_lookup)
            for r in records
        ]
        self.view.show_tournaments(tournaments)

    def manage_tournament(self):
        name = self.view.ask_tournament_name()
        if name is None:
            return

        record = tournaments_table.get(TournamentQuery.name == name)
        if not record:
            self.view.error_not_found()
            return

        players_lookup = self.player_controller.load_players_lookup()
        tournament = Tournament.from_dict(record, players_lookup)

        while True:
            choice = self.view.tournament_menu(tournament)
            if choice is None:
                return

            if choice == "1":
                self.round_controller.create_round(tournament)

            elif choice == "2":
                self.round_controller.enter_results(tournament)

            elif choice == "0":
                return
