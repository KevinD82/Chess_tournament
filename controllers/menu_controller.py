# controllers/menu_controller.py

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController

from rich.console import Console
from rich.panel import Panel

console = Console()


class MenuController:

    def __init__(self):
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.report_controller = ReportController()

    def run(self):
        while True:
            console.print(Panel.fit("[bold cyan]=== MENU PRINCIPAL ===[/bold cyan]"))

            console.print("1. Gestion des joueurs")
            console.print("2. Gestion des tournois")
            console.print("3. Rapports")
            console.print("0. Quitter\n")

            choice = console.input("[bold yellow]Votre choix : [/bold yellow]").strip()

            if choice == "1":
                self.menu_players()
            elif choice == "2":
                self.menu_tournaments()
            elif choice == "3":
                self.menu_reports()
            elif choice == "0":
                console.print("[green]Au revoir ![/green]")
                break
            else:
                console.print("[red]Choix invalide.[/red]")

    def menu_players(self):
        while True:
            console.print(Panel.fit("[bold cyan]=== GESTION DES JOUEURS ===[/bold cyan]"))

            console.print("1. Ajouter un joueur")
            console.print("2. Liste des joueurs")
            console.print("3. Supprimer un joueur")
            console.print("0. Retour\n")

            choice = console.input("[bold yellow]Votre choix : [/bold yellow]").strip()

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
            console.print(Panel.fit("[bold cyan]=== GESTION DES TOURNOIS ===[/bold cyan]"))

            console.print("1. Créer un tournoi")
            console.print("2. Liste des tournois")
            console.print("3. Lancer les matchs d’un tournoi")
            console.print("4. Supprimer un tournoi")
            console.print("0. Retour\n")

            choice = console.input("[bold yellow]Votre choix : [/bold yellow]").strip()

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
        while True:
            console.print(Panel.fit("[bold cyan]=== RAPPORTS ===[/bold cyan]"))

            console.print("1. Liste des tournois")
            console.print("2. Détails d’un tournoi")
            console.print("3. Historique complet")
            console.print("0. Retour\n")

            choice = console.input("[bold yellow]Votre choix : [/bold yellow]").strip()

            if choice == "1":
                self.report_controller.list_tournaments()
            elif choice == "2":
                self.report_controller.tournament_details()
            elif choice == "3":
                self.report_controller.full_history()
            elif choice == "0":
                return
            else:
                console.print("[red]Choix invalide.[/red]")
