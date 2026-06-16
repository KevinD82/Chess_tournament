# controllers/menu_controller.py

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController
from views.menu_view import MenuView
from rich.console import Console

console = Console()


class MenuController:
    """Contrôleur principal de navigation."""

    def __init__(self):
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.report_controller = ReportController()
        self.view = MenuView()

    def run(self):
        while True:
            choice = self.view.display_main_menu().strip()

            if choice == "1":
                self.menu_players()
            elif choice == "2":
                self.menu_tournaments()
            elif choice == "3":
                self.menu_reports()
            elif choice == "0":
                self.view.exit_message()
                break
            else:
                console.print("[red]Choix invalide.[/red]")

    def menu_players(self):
        while True:
            choice = self.view.display_player_menu().strip()

            if choice == "1":
                self.player_controller.create_player()
            elif choice == "2":
                self.player_controller.list_players()
            elif choice == "3":
                self.player_controller.delete_player()
            elif choice == "0":
                return
            else:
                console.print("[red]Choix invalide.[/red]")

    def menu_tournaments(self):
        while True:
            choice = self.view.display_tournament_menu().strip()

            if choice == "1":
                self.tournament_controller.create_tournament()
            elif choice == "2":
                self.tournament_controller.list_tournaments()
            elif choice == "3":
                self.tournament_controller.manage_tournament()
            elif choice == "4":
                self.tournament_controller.delete_tournament()
            elif choice == "0":
                return
            else:
                console.print("[red]Choix invalide.[/red]")

    def menu_reports(self):
        """Délègue la gestion des rapports au sous-contrôleur dédié."""
        # On quitte l'ancienne boucle locale pour exécuter la logique 
        # et le menu à 4 choix du ReportController
        self.report_controller.run()