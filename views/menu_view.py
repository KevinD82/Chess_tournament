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
        console.print(Panel.fit(
            "[bold cyan]=== MENU PRINCIPAL ===[/bold cyan]\n\n"
            "1. Gestion des joueurs\n"
            "2. Gestion des tournois\n"
            "3. Rapports\n"
            "0. Quitter"
        ))

    # --------------------------------------------------------------
    # Menu joueurs
    # --------------------------------------------------------------
    def display_player_menu(self):
        console.print(Panel.fit(
            "[bold cyan]=== GESTION DES JOUEURS ===[/bold cyan]\n\n"
            "1. Créer un joueur\n"
            "2. Liste des joueurs\n"
            "3. Supprimer un joueur\n"
            "0. Retour"
        ))

    # --------------------------------------------------------------
    # Menu tournois
    # --------------------------------------------------------------
    def display_tournament_menu(self):
        console.print(Panel.fit(
            "[bold cyan]=== GESTION DES TOURNOIS ===[/bold cyan]\n\n"
            "1. Créer un tournoi\n"
            "2. Liste des tournois\n"
            "3. Gérer un tournoi\n"
            "4. Supprimer un tournoi\n"
            "0. Retour"
        ))

    # --------------------------------------------------------------
    # Menu rapports
    # --------------------------------------------------------------
    def display_report_menu(self):
        console.print(Panel.fit(
            "[bold cyan]=== RAPPORTS ===[/bold cyan]\n\n"
            "1. Liste des joueurs\n"
            "2. Liste des tournois\n"
            "3. Détails d’un tournoi\n"
            "4. Rounds d’un tournoi\n"
            "5. Matchs d’un tournoi\n"
            "6. Scores d’un tournoi\n"
            "7. Historique complet\n"
            "0. Retour"
        ))

    # --------------------------------------------------------------
    # Message de sortie
    # --------------------------------------------------------------
    def exit_message(self):
        console.print("[green]Au revoir ![/green]")
