# views/report_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class ReportView:

    def safe_input(self, message):
        value = console.input(message)
        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée, retour au menu.[/yellow]")
            return None
        return value

    def ask_tournament_name(self):
        return self.safe_input("[yellow]Nom du tournoi : [/yellow]")

    def error_not_found(self):
        console.print("[red]Tournoi introuvable.[/red]")

    def show_players(self, players):
        table = Table(title="Liste des joueurs")
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("ID", style="magenta")
        table.add_column("Score", style="green")
        for p in players:
            table.add_row(p.last_name, p.first_name, p.national_id, str(p.score))
        console.print(table)

    def show_tournaments(self, tournaments):
        table = Table(title="Tournois enregistrés")
        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="magenta")
        table.add_column("Dates", style="green")
        for t in tournaments:
            table.add_row(t.name, t.location, f"{t.start_date} → {t.end_date}")
        console.print(table)

    def show_tournament_details(self, tournament):
        console.print(
            Panel.fit(
                f"[bold cyan]{tournament.name}[/bold cyan]\n"
                f"Lieu : {tournament.location}\n"
                f"Dates : {tournament.start_date} → {tournament.end_date}\n"
                f"Description : {tournament.description}",
                border_style="cyan"
            )
        )

    def show_rounds(self, rounds):
        table = Table(title="Rounds du tournoi")
        table.add_column("Nom", style="cyan")
        table.add_column("Début", style="green")
        table.add_column("Fin", style="green")
        for r in rounds:
            table.add_row(r.name, r.start_time, r.end_time or "-")
        console.print(table)

    def show_matches(self, rounds):
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

    def show_final_scores(self, players):
        players_sorted = sorted(players, key=lambda p: p.score, reverse=True)
        table = Table(title="Classement final")
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("Score", style="green")
        for p in players_sorted:
            table.add_row(p.last_name, p.first_name, str(p.score))
        console.print(table)

    def show_full_history(self, tournament):
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
