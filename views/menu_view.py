from rich.console import Console

console = Console()


class MenuView:
    """Affichage des menus."""

    def display_main_menu(self):
        console.print("\n[bold cyan]=== MENU PRINCIPAL ===[/bold cyan]")
        console.print("1. Gestion des joueurs")
        console.print("2. Gestion des tournois")
        console.print("3. Rapports")
        console.print("0. Quitter\n")
        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    def display_player_menu(self):
        console.print("\n[bold cyan]=== GESTION DES JOUEURS ===[/bold cyan]")
        console.print("1. Créer un joueur")
        console.print("2. Liste des joueurs")
        console.print("3. Supprimer un joueur")
        console.print("0. Retour\n")
        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    def display_tournament_menu(self):
        console.print("\n[bold cyan]=== GESTION DES TOURNOIS ===[/bold cyan]")
        console.print("1. Créer un tournoi")
        console.print("2. Liste des tournois")
        console.print("3. Piloter un tournoi")
        console.print("4. Supprimer un tournoi")
        console.print("0. Retour\n")
        return console.input("[bold yellow]Votre choix : [/bold yellow]")

    def exit_message(self):
        console.print("[green]Au revoir ![/green]")
