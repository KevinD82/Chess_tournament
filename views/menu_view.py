# views/menu_view.py

from rich.console import Console
from rich.panel import Panel

console = Console()


class MenuView:
    """
    Vue responsable de l'affichage du menu principal et du menu des rapports.
    """

    # --------------------------------------------------------------
    # Menu principal
    # --------------------------------------------------------------
    def main_menu(self):
        console.print(Panel.fit("[bold cyan]Menu Principal[/bold cyan]"))

        console.print("1. Créer un joueur")
        console.print("2. Liste des joueurs")
        console.print("3. Créer un tournoi")
        console.print("4. Liste des tournois")
        console.print("5. Gérer un tournoi")
        console.print("6. Rapports")
        console.print("7. Supprimer un joueur")
        console.print("0. Quitter\n")

        return console.input("[yellow]Votre choix : [/yellow]")

    # --------------------------------------------------------------
    # Menu des rapports
    # --------------------------------------------------------------
    def report_menu(self):
        console.print(Panel.fit("[bold cyan]Menu des rapports[/bold cyan]"))

        console.print("1. Liste des joueurs")
        console.print("2. Liste des tournois")
        console.print("3. Détails d’un tournoi")
        console.print("4. Rounds d’un tournoi")
        console.print("5. Matchs d’un tournoi")
        console.print("6. Scores d’un tournoi")
        console.print("7. Historique complet")
        console.print("0. Retour\n")

        return console.input("[yellow]Votre choix : [/yellow]")

    # --------------------------------------------------------------
    # Message de sortie
    # --------------------------------------------------------------
    def exit_message(self):
        console.print("[green]Au revoir ![/green]")
