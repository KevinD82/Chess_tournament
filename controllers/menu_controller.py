# controllers/menu_controller.py

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from views.menu_view import MenuView


class MenuController:

    def __init__(self):
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.view = MenuView()

    def run(self):
        while True:
            choice = self.view.main_menu()

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

            elif choice == "0":
                self.view.exit_message()
                break
