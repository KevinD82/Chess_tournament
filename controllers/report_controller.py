# controllers/report_controller.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from database import tournaments_table, TournamentQuery, players_table
from models.tournament import Tournament
from models.player import Player

console = Console()


class ReportController:

    # --------------------------------------------------------------
    # Menu principal des rapports
    # --------------------------------------------------------------
    def run(self):
        while True:
            console.print(Panel.fit(
                "[bold cyan]=== MENU DES RAPPORTS ===[/bold cyan]\n\n"
                "1. Liste des joueurs (ordre alphabétique)\n"
                "2. Liste des tournois\n"
                "3. Rapport complet d’un tournoi\n"
                "0. Retour"
            ))

            choice = console.input("Votre choix : ")

            if choice == "1":
                self.report_players()

            elif choice == "2":
                self.report_tournaments()

            elif choice == "3":
                self.report_one_tournament()

            elif choice == "0":
                return

    # --------------------------------------------------------------
    # Rapport : liste des joueurs
    # --------------------------------------------------------------
    def report_players(self):
        players = [Player.from_dict(p) for p in players_table.all()]
        players.sort(key=lambda p: (p.last_name.lower(), p.first_name.lower()))

        table = Table(title="Joueurs (ordre alphabétique)")
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("ID", style="magenta")

        for p in players:
            table.add_row(p.last_name, p.first_name, p.national_id)

        console.print(table)

    # --------------------------------------------------------------
    # Rapport : liste des tournois
    # --------------------------------------------------------------
    def report_tournaments(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        table = Table(title="Liste des tournois")
        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="yellow")
        table.add_column("Dates", style="magenta")

        for t in tournaments:
            table.add_row(
                t.name,
                t.location,
                f"{t.start_date} → {t.end_date}"
            )

        console.print(table)

    # --------------------------------------------------------------
    # Rapport complet d’un tournoi
    # --------------------------------------------------------------
    def report_one_tournament(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi disponible.[/yellow]")
            return

        # Sélection du tournoi
        table = Table(title="Sélection du tournoi")
        table.add_column("N°", style="yellow")
        table.add_column("Nom", style="cyan")

        for i, t in enumerate(tournaments, start=1):
            table.add_row(str(i), t.name)

        console.print(table)

        choice = console.input("Numéro du tournoi : ")

        try:
            tournament = tournaments[int(choice) - 1]
        except:
            console.print("[red]Choix invalide.[/red]")
            return

        # Recharger les joueurs
        all_players = [Player.from_dict(p) for p in players_table.all()]
        lookup = {p.national_id: p for p in all_players}

        # ----------------------------------------------------------
        # AFFICHAGE DU RAPPORT
        # ----------------------------------------------------------
        console.print(Panel.fit(
            f"[bold cyan]=== RAPPORT DU TOURNOI ===[/bold cyan]\n\n"
            f"[white]Nom :[/white] {tournament.name}\n"
            f"[white]Lieu :[/white] {tournament.location}\n"
            f"[white]Dates :[/white] {tournament.start_date} → {tournament.end_date}\n"
            f"[white]Description :[/white] {tournament.description}"
        ))

        # ----------------------------------------------------------
        # CLASSEMENT FINAL
        # ----------------------------------------------------------
        if tournament.final_ranking:
            text = "[bold green]=== CLASSEMENT FINAL ===[/bold green]\n\n"

            for i, (pid, score) in enumerate(tournament.final_ranking, start=1):
                p = lookup.get(pid)
                if p:
                    text += f"{i}. {p.first_name} {p.last_name} ({pid}) — {score} pts\n"

            console.print(Panel.fit(text))
        else:
            console.print("[yellow]Aucun classement final disponible.[/yellow]")

        # ----------------------------------------------------------
        # ROUNDS + MATCHS
        # ----------------------------------------------------------
        for r in tournament.rounds:
            console.print(Panel.fit(f"[cyan]{r.name}[/cyan]"))

            for m in r.matches:
                p1 = lookup.get(m.player1)
                p2 = lookup.get(m.player2)

                name1 = f"{p1.first_name} {p1.last_name}" if p1 else m.player1
                name2 = f"{p2.first_name} {p2.last_name}" if p2 else m.player2

                console.print(f"{name1} vs {name2} → {m.score1} / {m.score2}")
