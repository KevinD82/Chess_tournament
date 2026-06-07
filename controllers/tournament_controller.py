# controllers/tournament_controller.py

from models.tournament import Tournament
from database import tournaments_table, players_table
from views.tournament_view import TournamentView
from tinydb import where
from datetime import datetime

from rich.console import Console
console = Console()


class TournamentController:

    def __init__(self):
        self.view = TournamentView()

    def create_tournament(self):
        data = self.view.ask_tournament_info()
        tournament = Tournament(**data)

        players = players_table.all()[:4]
        tournament.players = [p["last_name"] + " " + p["first_name"] for p in players]

        tournaments_table.insert(tournament.to_dict())
        console.print("[green]Tournoi créé avec succès ![/green]")

    def list_tournaments(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        self.view.show_tournaments(tournaments)

    def manage_tournament(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        self.view.show_tournaments(tournaments)

        while True:
            choice = console.input("Numéro du tournoi à gérer : ").strip()

            if not choice.isdigit():
                console.print("[red]Numéro invalide.[/red]")
                continue

            index = int(choice) - 1

            if index < 0 or index >= len(tournaments):
                console.print("[red]Numéro hors liste.[/red]")
                continue

            tournament = tournaments[index]
            break

        # Heure de début automatique
        tournament.start_time = datetime.now().strftime("%H:%M")

        players = tournament.players
        if len(players) < 4:
            console.print("[red]Il faut au moins 4 joueurs.[/red]")
            return

        rounds = [
            [(players[0], players[1]), (players[2], players[3])],
            [(players[0], players[2]), (players[1], players[3])],
            [(players[0], players[3]), (players[1], players[2])]
        ]

        scores = {p: 0 for p in players}
        tournament.rounds = []

        for i, matches in enumerate(rounds, start=1):
            self.view.show_round(i, [{"p1": m[0], "p2": m[1]} for m in matches])

            round_data = []

            for p1, p2 in matches:
                s1, s2 = self.view.ask_score(p1, p2)
                scores[p1] += s1
                scores[p2] += s2

                round_data.append({"p1": p1, "p2": p2, "s1": s1, "s2": s2})

            tournament.rounds.append(round_data)

        tournament.results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Heure de fin automatique
        tournament.end_time = datetime.now().strftime("%H:%M")

        tournaments_table.update(tournament.to_dict(), where("name") == tournament.name)

        self.view.show_results(tournament.results)

    def delete_tournament(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        self.view.show_tournaments(tournaments)

        choice = console.input("Numéro du tournoi à supprimer : ").strip()

        if not choice.isdigit():
            console.print("[red]Choix invalide.[/red]")
            return

        index = int(choice) - 1

        if index < 0 or index >= len(tournaments):
            console.print("[red]Numéro hors liste.[/red]")
            return

        tournament = tournaments[index]

        tournaments_table.remove(where("name") == tournament.name)

        console.print(f"[green]Tournoi '{tournament.name}' supprimé ![/green]")
