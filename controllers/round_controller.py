# controllers/round_controller.py

from database import tournaments_table, TournamentQuery
from models.round import Round
from views.round_view import RoundView


class RoundController:

    def __init__(self):
        self.view = RoundView()

    def create_round(self, tournament):
        round_obj = Round.create_new(tournament)
        tournament.rounds.append(round_obj)
        tournaments_table.update(tournament.to_dict(), TournamentQuery.name == tournament.name)
        self.view.show_round(round_obj)

    def enter_results(self, tournament):
        if not tournament.rounds:
            return

        round_obj = tournament.rounds[-1]

        for match in round_obj.matches:
            result = self.view.ask_match_result(match)
            if result is None:
                return  # annulé

            score1, score2 = result
            match.score1 = score1
            match.score2 = score2

        tournaments_table.update(tournament.to_dict(), TournamentQuery.name == tournament.name)
        self.view.confirm_results_saved()
