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
        - "echap"
        - "escape"
        - "annuler"
        - "cancel"
        - "q"

        Alors la saisie est annulée et la méthode retourne None.
        """
        value = console.input(message)

        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée, retour au menu.[/yellow]")
            return None

        return value

    # ------------------------------------------------------------------
    # 2. Demande des informations pour créer un joueur
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

        # Les données sont retournées sous forme de dict
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
        """
        Affiche un message confirmant la création du joueur.
        """
        console.print(
            f"[green]Joueur {player.first_name} {player.last_name} créé avec succès ![/green]"
        )

    # ------------------------------------------------------------------
    # 4. Affichage de la liste des joueurs
    # ------------------------------------------------------------------
    def show_players(self, players):
        """
        Affiche la liste des joueurs dans un tableau Rich.

        players : liste d'objets Player
        """
        table = Table(title="Liste des joueurs")

        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("ID National", style="magenta")
        table.add_column("Score", style="green")

        # Ajout de chaque joueur dans le tableau
        for p in players:
            table.add_row(p.last_name, p.first_name, p.national_id, str(p.score))

        console.print(table)
