# views/report_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Console Rich utilisée pour afficher du texte stylé dans le terminal
console = Console()


class ReportView:
    """
    Vue dédiée à l'affichage des rapports :
    - liste des joueurs
    - liste des tournois
    - détails d’un tournoi
    - rounds
    - matchs
    - scores finaux
    - historique complet

    Cette vue ne contient aucune logique métier :
    elle affiche uniquement les données fournies par ReportController.
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
    # 2. Demande du nom du tournoi
    # ------------------------------------------------------------------
    def ask_tournament_name(self):
        """
        Demande à l'utilisateur le nom du tournoi pour afficher un rapport.
        """
        return self.safe_input("[yellow]Nom du tournoi : [/yellow]")

    # ------------------------------------------------------------------
    # 3. Message d'erreur si tournoi introuvable
    # ------------------------------------------------------------------
    def error_not_found(self):
        """
        Affiche un message d'erreur si le tournoi demandé n'existe pas.
        """
        console.print("[red]Tournoi introuvable.[/red]")

    # ------------------------------------------------------------------
    # 4. Affichage de la liste des joueurs
    # ------------------------------------------------------------------
    def show_players(self, players):
        """
        Affiche la liste de tous les joueurs enregistrés.
        """
        table = Table(title="Liste des joueurs")

        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("ID", style="magenta")
        table.add_column("Score", style="green")

        for p in players:
            table.add_row(p.last_name, p.first_name, p.national_id, str(p.score))

        console.print(table)

    # ------------------------------------------------------------------
    # 5. Affichage de la liste des tournois
    # ------------------------------------------------------------------
    def show_tournaments(self, tournaments):
        """
        Affiche tous les tournois enregistrés dans TinyDB.
        """
        table = Table(title="Tournois enregistrés")

        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="magenta")
        table.add_column("Dates", style="green")

        for t in tournaments:
            table.add_row(t.name, t.location, f"{t.start_date} → {t.end_date}")

        console.print(table)

    # ------------------------------------------------------------------
    # 6. Affichage des détails d’un tournoi
    # ------------------------------------------------------------------
    def show_tournament_details(self, tournament):
        """
        Affiche les informations générales d’un tournoi :
        - nom
        - lieu
        - dates
        - description
        """
        console.print(
            Panel.fit(
                f"[bold cyan]{tournament.name}[/bold cyan]\n"
                f"Lieu : {tournament.location}\n"
                f"Dates : {tournament.start_date} → {tournament.end_date}\n"
                f"Description : {tournament.description}",
                border_style="cyan"
            )
        )

    # ------------------------------------------------------------------
    # 7. Affichage des rounds d’un tournoi
    # ------------------------------------------------------------------
    def show_rounds(self, rounds):
        """
        Affiche la liste des rounds d’un tournoi.
        """
        table = Table(title="Rounds du tournoi")

        table.add_column("Nom", style="cyan")
        table.add_column("Début", style="green")
        table.add_column("Fin", style="green")

        for r in rounds:
            table.add_row(r.name, r.start_time, r.end_time or "-")

        console.print(table)

    # ------------------------------------------------------------------
    # 8. Affichage des matchs d’un tournoi
    # ------------------------------------------------------------------
    def show_matches(self, rounds):
        """
        Affiche tous les matchs d’un tournoi, round par round.
        """
        for r in rounds:
            table = Table(title=f"Matchs du {r.name}")

            table.add_column("Joueur 1", style="cyan")
            table.add_column("Score", style="yellow")
            table.add_column("Joueur 2", style="cyan")
            table.add_column("Score", style="yellow")

            for m in r.matches:
                table.add_row(
                    f"{m.player1.first_name} {m.player1.last_name}",
                    str(m.score1),
                    f"{m.player2.first_name} {m.player2.last_name}",
                    str(m.score2),
                )

            console.print(table)

    # ------------------------------------------------------------------
    # 9. Affichage du classement final
    # ------------------------------------------------------------------
    def show_final_scores(self, players):
        """
        Affiche les joueurs triés par score décroissant.
        """
        players_sorted = sorted(players, key=lambda p: p.score, reverse=True)

        table = Table(title="Classement final")

        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("Score", style="green")

        for p in players_sorted:
            table.add_row(p.last_name, p.first_name, str(p.score))

        console.print(table)

    # ------------------------------------------------------------------
    # 10. Affichage de l’historique complet d’un tournoi
    # ------------------------------------------------------------------
    def show_full_history(self, tournament):
        """
        Affiche :
        - les détails du tournoi
        - les rounds
        - les matchs
        - le classement final

        C’est le rapport le plus complet.
        """
        console.print(
            Panel.fit(
                f"[bold cyan]Historique complet du tournoi : {tournament.name}[/bold cyan]",
                border_style="cyan"
            )
        )

        self.show_tournament_details(tournament)
        self.show_rounds(tournament.rounds)
        self.show_matches(tournament.rounds)
        self.show_final_scores(tournament.players)
