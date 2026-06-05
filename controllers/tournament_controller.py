# controllers/tournament_controller.py

from models.tournament import Tournament
from database import tournaments_table, players_table
from views.tournament_view import TournamentView
from tinydb import where

from rich.console import Console
console = Console()


class TournamentController:

    def __init__(self):
        self.view = TournamentView()

    # --------------------------------------------------------------
    # Création d’un tournoi
    # --------------------------------------------------------------
    def create_tournament(self):
        data = self.view.ask_tournament_info()
        tournament = Tournament(**data)

        # Sélection automatique des 4 premiers joueurs
        players = players_table.all()[:4]
        tournament.players = [p["last_name"] + " " + p["first_name"] for p in players]

        tournaments_table.insert(tournament.to_dict())
        console.print("[green]Tournoi créé avec 4 joueurs automatiquement sélectionnés.[/green]")

    # --------------------------------------------------------------
    # Liste des tournois
    # --------------------------------------------------------------
    def list_tournaments(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        self.view.show_tournaments(tournaments)

    # --------------------------------------------------------------
    # Gestion du tournoi (Round Robin 4 joueurs)
    # --------------------------------------------------------------
    def manage_tournament(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        self.view.show_tournaments(tournaments)

        choice = input("Numéro du tournoi à gérer : ").strip()
        if not choice.isdigit():
            console.print("[red]Choix invalide.[/red]")
            return

        tournament = tournaments[int(choice) - 1]

        players = tournament.players
        if len(players) < 4:
            console.print("[red]Il faut au moins 4 joueurs.[/red]")
            return

        # Round Robin (3 rounds)
        rounds = [
            [(players[0], players[1]), (players[2], players[3])],
            [(players[0], players[2]), (players[1], players[3])],
            [(players[0], players[3]), (players[1], players[2])]
        ]

        scores = {p: 0 for p in players}
        tournament.rounds = []  # IMPORTANT

        for i, matches in enumerate(rounds, start=1):
            self.view.show_round(i, [{"p1": m[0], "p2": m[1]} for m in matches])

            round_data = []

            for p1, p2 in matches:
                s1, s2 = self.view.ask_score(p1, p2)

                scores[p1] += s1
                scores[p2] += s2

                round_data.append({
                    "p1": p1,
                    "p2": p2,
                    "s1": s1,
                    "s2": s2
                })

            tournament.rounds.append(round_data)

        # Classement final
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        tournament.results = sorted_results

        # Sauvegarde
        tournaments_table.update(tournament.to_dict(), where("name") == tournament.name)

        self.view.show_results(sorted_results)

    # --------------------------------------------------------------
    # Suppression d’un tournoi
    # --------------------------------------------------------------
    def delete_tournament(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        self.view.show_tournaments(tournaments)

        choice = input("Numéro du tournoi à supprimer : ").strip()

        if not choice.isdigit():
            console.print("[red]Choix invalide.[/red]")
            return

        index = int(choice) - 1

        if index < 0 or index >= len(tournaments):
            console.print("[red]Numéro hors liste.[/red]")
            return

        tournament = tournaments[index]

        tournaments_table.remove(where("name") == tournament.name)

        console.print(f"[green]Tournoi '{tournament.name}' supprimé avec succès ![/green]")
