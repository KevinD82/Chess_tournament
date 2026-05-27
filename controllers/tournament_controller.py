# controllers/tournament_controller.py

from models.tournament import Tournament
from database import tournaments_table, TournamentQuery
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController
from views.tournament_view import TournamentView


class TournamentController:

    def __init__(self):
        self.player_controller = PlayerController()
        self.round_controller = RoundController()
        self.view = TournamentView()

    def create_tournament(self):
        data = self.view.ask_tournament_info()
        players = self.player_controller.load_players_lookup()

        selected_players = self.view.select_players(list(players.values()))

        tournament = Tournament(
            players=selected_players,
            **data
        )

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
        record = tournaments_table.get(TournamentQuery.name == name)

        if not record:
            self.view.error_not_found()
            return

        players_lookup = self.player_controller.load_players_lookup()
        tournament = Tournament.from_dict(record, players_lookup)

        while True:
            choice = self.view.tournament_menu(tournament)

            if choice == "1":
                new_round = tournament.create_round()
                self.view.show_round(new_round)
                tournaments_table.update(tournament.to_dict(), TournamentQuery.name == name)

            elif choice == "2":
                self.round_controller.enter_results(tournament)
                tournaments_table.update(tournament.to_dict(), TournamentQuery.name == name)

            elif choice == "0":
                break
