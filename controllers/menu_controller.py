from rich.console import Console
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController
from views.tournament_view import TournamentView
from views.player_view import PlayerView

console = Console()


class MenuController:
    """Menu principal et navigation générale."""

    def __init__(self):
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.report_controller = ReportController()
        self.tournament_view = TournamentView()
        self.player_view = PlayerView()

    def run(self):
        while True:
            console.print("\n[bold cyan]=== MENU PRINCIPAL ===[/bold cyan]")
            console.print("1. Gestion des joueurs")
            console.print("2. Gestion des tournois")
            console.print("3. Rapports")
            console.print("0. Quitter")

            choice = console.input("\n[bold yellow]Votre choix : [/bold yellow]").strip()

            if choice == "1":
                self.player_menu()
            elif choice == "2":
                self.tournament_menu()
            elif choice == "3":
                self.report_menu()
            elif choice == "0":
                console.print("[green]Au revoir ![/green]")
                break
            else:
                console.print("[red]Choix invalide.[/red]")

    def player_menu(self):
        while True:
            console.print("\n[bold cyan]=== GESTION DES JOUEURS ===[/bold cyan]")
            console.print("1. Créer un joueur")
            console.print("2. Liste des joueurs")
            console.print("3. Supprimer un joueur")
            console.print("0. Retour")

            choice = console.input("\n[bold yellow]Votre choix : [/bold yellow]").strip()

            if choice == "1":
                self.player_controller.create_player()
            elif choice == "2":
                self.player_controller.list_players()
            elif choice == "3":
                self.player_controller.delete_player()
            elif choice == "0":
                break
            else:
                console.print("[red]Choix invalide.[/red]")

    def tournament_menu(self):
        while True:
            choice = self.tournament_view.display_tournament_menu()

            if choice == "1":
                self.tournament_controller.create_tournament()
            elif choice == "2":
                self.tournament_controller.list_tournaments()
            elif choice == "3":
                self.tournament_controller.add_players_to_tournament()
            elif choice == "4":
                self.tournament_controller.manage_tournament()
            elif choice == "5":
                self.tournament_controller.delete_tournament()
            elif choice == "0":
                break
            else:
                console.print("[red]Choix invalide.[/red]")

    def report_menu(self):
        while True:
            console.print("\n[bold cyan]=== RAPPORTS ===[/bold cyan]")
            console.print("1. Liste des tournois")
            console.print("2. Détail d’un tournoi")
            console.print("3. Historique complet")
            console.print("0. Retour")

            choice = console.input("\n[bold yellow]Votre choix : [/bold yellow]").strip()

            if choice == "1":
                self.report_controller.report_tournaments()
            elif choice == "2":
                self.report_controller.report_tournament_details()
            elif choice == "3":
                self.report_controller.report_full_history()
            elif choice == "0":
                break
            else:
                console.print("[red]Choix invalide.[/red]")
