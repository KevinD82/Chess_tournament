# views/menu_view.py

from rich.console import Console
from rich.panel import Panel

# Console Rich utilisée pour afficher du texte stylé dans le terminal
console = Console()


class MenuView:
    """
    Vue responsable de l'affichage du menu principal et du menu des rapports.
    Elle ne contient aucune logique métier : uniquement de l'affichage
    et de la récupération de saisie utilisateur.
    """

    # ------------------------------------------------------------------
    # 1. Menu principal
    # ------------------------------------------------------------------
    def main_menu(self):
        """
        Affiche le menu principal de l'application.
        Retourne le choix de l'utilisateur sous forme de string.
        """
        console.print(Panel.fit("[bold cyan]Menu Principal[/bold cyan]"))

        console.print("1. Créer un joueur")
        console.print("2. Liste des joueurs")
        console.print("3. Créer un tournoi")
        console.print("4. Liste des tournois")
        console.print("5. Gérer un tournoi")
        console.print("6. Rapports")
        console.print("0. Quitter\n")

        # console.input() permet d'afficher une invite stylée
        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    # ------------------------------------------------------------------
    # 2. Menu des rapports
    # ------------------------------------------------------------------
    def report_menu(self):
        """
        Affiche le sous-menu dédié aux rapports.
        Retourne le choix de l'utilisateur.
        """
        console.print(Panel.fit("[bold cyan]Rapports[/bold cyan]"))

        console.print("1. Liste de tous les joueurs")
        console.print("2. Liste de tous les tournois")
        console.print("3. Détails d’un tournoi")
        console.print("4. Rounds d’un tournoi")
        console.print("5. Matchs d’un tournoi")
        console.print("6. Scores finaux d’un tournoi")
        console.print("7. Historique complet d’un tournoi")
        console.print("0. Retour\n")

        return console.input("[yellow]Votre choix : [/yellow]")

    # ------------------------------------------------------------------
    # 3. Message de sortie
    # ------------------------------------------------------------------
    def exit_message(self):
        """
        Affiche un message de remerciement lorsque l'utilisateur quitte l'application.
        """
        console.print("\n[green]Merci d'avoir utilisé Chess Tournament Manager ![/green]\n")
