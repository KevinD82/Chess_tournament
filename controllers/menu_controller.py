# controllers/menu_controller.py

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController
from views.menu_view import MenuView


class MenuController:

    def __init__(self):
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.report_controller = ReportController()
        self.view = MenuView()

    def run(self):
        while True:
            choice = self.view.main_menu()

            if choice is None:
                continue  # utilisateur a fait "echap"

            if choice == "1":
                self.player_controller.create_player()

            elif choice == "2":
                self.player_controller.list_players()

            elif choice == "3":
                self.tournament_controller.create_tournament()

            elif choice == "4":
                self.tournament_controller.list_tournaments()

            elif choice == "5":
                self.tournament_controller.manage_tournament()

            elif choice == "6":
                self.report_menu()

            elif choice == "0":
                self.view.exit_message()
                break

    def report_menu(self):
        while True:
            choice = self.view.report_menu()

            if choice is None:
                return  # retour au menu principal

            if choice == "1":
                self.report_controller.list_all_players()

            elif choice == "2":
                self.report_controller.list_all_tournaments()

            elif choice == "3":
                self.report_controller.tournament_details()

            elif choice == "4":
                self.report_controller.tournament_rounds()

            elif choice == "5":
                self.report_controller.tournament_matches()

            elif choice == "6":
                self.report_controller.tournament_scores()

            elif choice == "7":
                self.report_controller.full_history()

            elif choice == "0":
                return
