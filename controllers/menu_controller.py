# controllers/menu_controller.py

from rich.console import Console
from rich.panel import Panel

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController

console = Console()


class MenuController:

    def __init__(self):
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.report_controller = ReportController()

    # --------------------------------------------------------------
    # Menu principal
    # --------------------------------------------------------------
    def run(self):
        while True:
            console.print(Panel.fit(
                "[bold cyan]=== MENU PRINCIPAL ===[/bold cyan]\n\n"
                "1. Gestion des joueurs\n"
                "2. Gestion des tournois\n"
                "3. Rapports\n"
                "0. Quitter"
            ))

            choice = console.input("Votre choix : ")

            if choice == "1":
                self.menu_players()

            elif choice == "2":
                self.menu_tournaments()

            elif choice == "3":
                self.report_controller.run()

            elif choice == "0":
                console.print("[green]Au revoir ![/green]")
                return

            else:
                console.print("[red]Choix invalide.[/red]")

    # --------------------------------------------------------------
    # Menu joueurs
    # --------------------------------------------------------------
    def menu_players(self):
        while True:
            console.print(Panel.fit(
                "[bold cyan]=== GESTION DES JOUEURS ===[/bold cyan]\n\n"
                "1. Créer un joueur\n"
                "2. Liste des joueurs\n"
                "3. Supprimer un joueur\n"
                "0. Retour"
            ))

            choice = console.input("Votre choix : ")

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

    # --------------------------------------------------------------
    # Menu tournois
    # --------------------------------------------------------------
    def menu_tournaments(self):
        while True:
            console.print(Panel.fit(
                "[bold cyan]=== GESTION DES TOURNOIS ===[/bold cyan]\n\n"
                "1. Créer un tournoi\n"
                "2. Liste des tournois\n"
                "3. Gérer un tournoi\n"
                "4. Supprimer un tournoi\n"
                "0. Retour"
            ))

            choice = console.input("Votre choix : ")

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
