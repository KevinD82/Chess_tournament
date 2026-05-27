# views/player_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Console Rich utilisée pour afficher du texte stylé dans le terminal
console = Console()


class PlayerView:
    """
    Vue responsable de toutes les interactions utilisateur concernant les joueurs :
    - saisie des informations d’un joueur
    - affichage de confirmation
    - affichage de la liste des joueurs
    - affichage de confirmation de suppression

    Elle ne contient aucune logique métier : uniquement de l'affichage
    et de la récupération de saisie utilisateur.
    """

    # ------------------------------------------------------------------
    # 1. Saisie sécurisée (annulation possible)
    # ------------------------------------------------------------------
    def safe_input(self, message):
        """
        Demande une saisie utilisateur avec possibilité d'annuler.

        Si l'utilisateur tape :
        - echap / escape
        - annuler / cancel
        - q

        Alors la saisie est annulée et la méthode retourne None.
        """
        value = console.input(message)

        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée, retour au menu.[/yellow]")
            return None

        return value

    # ------------------------------------------------------------------
    # 2. Formulaire de création d’un joueur
    # ------------------------------------------------------------------
    def ask_player_info(self):
        """
        Affiche un formulaire de création de joueur.
        Chaque champ peut être annulé via safe_input().
        Retourne un dictionnaire prêt à être utilisé par Player(**data).
        """
        console.print(Panel.fit("[bold cyan]Création d'un joueur[/bold cyan]"))

        last_name = self.safe_input("Nom : ")
        if last_name is None:
            return None

        first_name = self.safe_input("Prénom : ")
        if first_name is None:
            return None

        birthdate = self.safe_input("Date de naissance (JJ/MM/AAAA) : ")
        if birthdate is None:
            return None

        national_id = self.safe_input("Identifiant national : ")
        if national_id is None:
            return None

        return {
            "last_name": last_name,
            "first_name": first_name,
            "birthdate": birthdate,
            "national_id": national_id
        }

    # ------------------------------------------------------------------
    # 3. Confirmation de création
    # ------------------------------------------------------------------
    def confirm_player_created(self, player):
        """Affiche un message confirmant la création du joueur."""
        console.print(f"[green]Joueur {player.first_name} {player.last_name} créé avec succès ![/green]")

    # ------------------------------------------------------------------
    # 4. Confirmation de suppression
    # ------------------------------------------------------------------
    def confirm_player_deleted(self, player):
        """Affiche un message confirmant la suppression du joueur."""
        console.print(f"[red]Joueur {player.first_name} {player.last_name} supprimé avec succès.[/red]")

    # ------------------------------------------------------------------
    # 5. Affichage de la liste des joueurs
    # ------------------------------------------------------------------
    def show_players(self, players):
        """
        Affiche la liste des joueurs dans un tableau Rich.
        Ajoute une colonne "N°" pour permettre la suppression par numéro.
        """
        table = Table(title="Liste des joueurs")

        table.add_column("N°", style="yellow")
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("ID National", style="magenta")
        table.add_column("Score", style="green")

        for i, p in enumerate(players, start=1):
            table.add_row(str(i), p.last_name, p.first_name, p.national_id, str(p.score))

        console.print(table)
