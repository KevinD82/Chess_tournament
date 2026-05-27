# views/tournament_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Console Rich pour un affichage stylé
console = Console()


class TournamentView:
    """
    Vue responsable de toutes les interactions utilisateur concernant les tournois :
    - saisie des informations d’un tournoi
    - sélection des joueurs
    - affichage de confirmation
    - affichage de la liste des tournois
    - menu de gestion d’un tournoi

    Cette vue ne contient aucune logique métier.
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
    # 2. Demande des informations pour créer un tournoi
    # ------------------------------------------------------------------
    def ask_tournament_info(self):
        """
        Affiche un formulaire de création de tournoi.
        Retourne un dictionnaire prêt à être utilisé par Tournament(**data).
        """
        console.print(Panel.fit("[bold cyan]Création d'un tournoi[/bold cyan]"))

        name = self.safe_input("Nom du tournoi : ")
        if name is None:
            return None

        location = self.safe_input("Lieu : ")
        if location is None:
            return None

        start_date = self.safe_input("Date de début (JJ/MM/AAAA) : ")
        if start_date is None:
            return None

        end_date = self.safe_input("Date de fin (JJ/MM/AAAA) : ")
        if end_date is None:
            return None

        description = self.safe_input("Description : ")
        if description is None:
            return None

        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
        }

    # ------------------------------------------------------------------
    # 3. Sélection des joueurs pour un tournoi
    # ------------------------------------------------------------------
    def select_players(self, players):
        """
        Affiche la liste des joueurs et permet d’en sélectionner plusieurs.

        players : liste d'objets Player
        Retourne une liste de joueurs sélectionnés.
        """
        console.print(Panel.fit("[bold cyan]Sélection des joueurs[/bold cyan]"))

        table = Table(title="Joueurs disponibles")
        table.add_column("Index", style="yellow")
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("ID", style="magenta")

        for i, p in enumerate(players):
            table.add_row(str(i), p.last_name, p.first_name, p.national_id)

        console.print(table)

        raw = self.safe_input(
            "Entrez les index des joueurs séparés par des virgules (ex: 0,2,5) : "
        )
        if raw is None:
            return None

        try:
            indexes = [int(x.strip()) for x in raw.split(",")]
        except ValueError:
            console.print("[red]Format invalide.[/red]")
            return None

        selected = []
        for idx in indexes:
            if 0 <= idx < len(players):
                selected.append(players[idx])
            else:
                console.print(f"[red]Index invalide : {idx}[/red]")

        return selected

    # ------------------------------------------------------------------
    # 4. Confirmation de création
    # ------------------------------------------------------------------
    def confirm_tournament_created(self, tournament):
        """
        Affiche un message confirmant la création du tournoi.
        """
        console.print(
            Panel.fit(
                f"[green]Tournoi '{tournament.name}' créé avec succès ![/green]",
                border_style="green"
            )
        )

    # ------------------------------------------------------------------
    # 5. Affichage de la liste des tournois
    # ------------------------------------------------------------------
    def show_tournaments(self, tournaments):
        """
        Affiche la liste des tournois enregistrés.
        """
        table = Table(title="Liste des tournois")

        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="magenta")
        table.add_column("Dates", style="green")

        for t in tournaments:
            table.add_row(t.name, t.location, f"{t.start_date} → {t.end_date}")

        console.print(table)

    # ------------------------------------------------------------------
    # 6. Menu de gestion d’un tournoi
    # ------------------------------------------------------------------
    def tournament_menu(self, tournament):
        """
        Affiche le menu de gestion d’un tournoi :
        - créer un round
        - saisir les résultats
        - retour
        """
        console.print(
            Panel.fit(
                f"[bold cyan]Gestion du tournoi : {tournament.name}[/bold cyan]",
                border_style="cyan"
            )
        )

        console.print("1. Créer un round")
        console.print("2. Saisir les résultats du round en cours")
        console.print("0. Retour\n")

        return console.input("[yellow]Votre choix : [/yellow]")
