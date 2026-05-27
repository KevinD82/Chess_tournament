# controllers/round_controller.py

from views.round_view import RoundView


class RoundController:

    def __init__(self):
        self.view = RoundView()

    def enter_results(self, tournament):
        current_round = tournament.rounds[-1]

        for match in current_round.matches:
            score1, score2 = self.view.ask_match_result(match)
            match.set_scores(score1, score2)

        current_round.end_round()
        tournament.update_scores(current_round)
        self.view.confirm_results_saved()
