# views/menu_view.py

from rich.console import Console
from rich.panel import Panel

console = Console()


class MenuView:
    """
    Vue responsable de l'affichage des menus.
    Elle ne contient aucune logique métier.
    """

    # --------------------------------------------------------------
    # Menu principal
    # --------------------------------------------------------------
    def display_main_menu(self):
        console.print(Panel.fit("[bold cyan]=== MENU PRINCIPAL ===[/bold cyan]"))

        console.print("1. Gestion des joueurs")
        console.print("2. Gestion des tournois")
        console.print("3. Rapports")
        console.print("0. Quitter\n")

        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    # --------------------------------------------------------------
    # Menu joueurs
    # --------------------------------------------------------------
    def display_player_menu(self):
        console.print(Panel.fit("[bold cyan]=== GESTION DES JOUEURS ===[/bold cyan]"))

        console.print("1. Créer un joueur")
        console.print("2. Liste des joueurs")
        console.print("3. Supprimer un joueur")
        console.print("0. Retour\n")

        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    # --------------------------------------------------------------
    # Menu tournois
    # --------------------------------------------------------------
    def display_tournament_menu(self):
        console.print(Panel.fit("[bold cyan]=== GESTION DES TOURNOIS ===[/bold cyan]"))

        console.print("1. Créer un tournoi")
        console.print("2. Liste des tournois")
        console.print("3. Gérer un tournoi")
        console.print("4. Supprimer un tournoi")
        console.print("0. Retour\n")

        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    # --------------------------------------------------------------
    # Menu rapports
    # --------------------------------------------------------------
    def display_report_menu(self):
        console.print(Panel.fit("[bold cyan]=== RAPPORTS ===[/bold cyan]"))

        console.print("1. Liste des joueurs")
        console.print("2. Liste des tournois")
        console.print("3. Détails d’un tournoi")
        console.print("4. Rounds d’un tournoi")
        console.print("5. Matchs d’un tournoi")
        console.print("6. Scores d’un tournoi")
        console.print("7. Historique complet")
        console.print("0. Retour\n")

        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    # --------------------------------------------------------------
    # Message de sortie
    # --------------------------------------------------------------
    def exit_message(self):
        console.print("[green]Au revoir ![/green]")
