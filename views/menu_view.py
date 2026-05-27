# views/menu_view.py

from rich.console import Console
from rich.panel import Panel

console = Console()


class MenuView:

    def main_menu(self):
        console.print(Panel.fit("[bold cyan]Menu Principal[/bold cyan]"))

        console.print("1. Créer un joueur")
        console.print("2. Liste des joueurs")
        console.print("3. Créer un tournoi")
        console.print("4. Liste des tournois")
        console.print("5. Gérer un tournoi")
        console.print("6. Rapports")
        console.print("0. Quitter\n")

        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    def report_menu(self):
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

    def exit_message(self):
        console.print("\n[green]Merci d'avoir utilisé Chess Tournament Manager ![/green]\n")
