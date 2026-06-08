# views/menu_view.py

from rich.console import Console
from rich.panel import Panel

console = Console()


class MenuView:

    # Vue de l'affichage des menus.
    # Cette classe est responsable de l'affichage de tous les menus et messages à l'utilisateur.

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
        console.print("3. Lancer les matchs d’un tournoi")
        console.print("4. Supprimer un tournoi")
        console.print("0. Retour\n")

        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    # --------------------------------------------------------------
    # Menu rapports
    # --------------------------------------------------------------
    def display_report_menu(self):
        console.print(Panel.fit("[bold cyan]=== RAPPORTS ===[/bold cyan]"))

        console.print("1. Liste des tournois")
        console.print("2. Détails d’un tournoi")
        console.print("3. Historique complet")
        console.print("0. Retour\n")

        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    # --------------------------------------------------------------
    # Message de sortie
    # --------------------------------------------------------------
    def exit_message(self):
        console.print("[green]Au revoir ![/green]")
