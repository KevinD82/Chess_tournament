# controllers/tournament_controller.py

import random
from datetime import datetime
from tinydb import where
from rich.console import Console

from models.tournament import Tournament
from models.round import Round
from models.match import Match
from database import tournaments_table, players_table
from views.tournament_view import TournamentView
from controllers.round_controller import RoundController

console = Console()


class TournamentController:

    def __init__(self):
        self.view = TournamentView()
        self.round_controller = RoundController()

    def create_tournament(self):
        all_players = players_table.all()

        # Bloque la création s'il n'y a pas le quota de joueurs requis
        if len(all_players) < 4:
            console.print("\n[red]❌ Erreur : Impossible de créer un tournoi.[/red]")
            console.print(f"[yellow]Le système ne contient que {len(all_players)} joueur(s).[/yellow]")
            console.print("[yellow]Veuillez d'abord enregistrer au moins 4 joueurs dans le menu principal.[/yellow]\n")
            return

        data = self.view.ask_tournament_info()
        tournament = Tournament(**data)

        # Sélection automatique des 4 premiers joueurs
        tournament.players = [p["last_name"] + " " + p["first_name"] for p in all_players[:4]]

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
                console.print("[red]Choix invalide.[/red]")
                continue
            index = int(choice) - 1
            if index < 0 or index >= len(tournaments):
                console.print("[red]Numéro hors liste.[/red]")
                continue
            tournament = tournaments[index]
            break

        if not tournament.start_time:
            tournament.start_time = datetime.now().strftime("%H:%M")

        if not tournament.rounds:
            # Mélange initial unique pour varier l'ordre des confrontations à chaque tournoi
            plist = list(tournament.players)
            random.shuffle(plist)

            # Algorithme mathématique de rotation pour 4 joueurs (Toutes rondes - Confrontation unique)
            aller_rounds_paires = [
                [(plist[0], plist[3]), (plist[1], plist[2])],  # Round 1
                [(plist[0], plist[2]), (plist[3], plist[1])],  # Round 2
                [(plist[0], plist[1]), (plist[2], plist[3])]   # Round 3
            ]

            # --- SÉQUENCE DES MATCHS UNIQUES (Rounds 1 à 3) ---
            for i, paires in enumerate(aller_rounds_paires, start=1):
                round_obj = Round(f"Round {i}")
                for p1, p2 in paires:
                    round_obj.matches.append(Match(p1, p2))

                tournament.rounds.append(round_obj.to_dict())
                self.view.show_round(i, round_obj.matches)
                self.round_controller.enter_results(tournament)

        else:
            console.print("[yellow]Ce tournoi a déjà été joué ou est en cours.[/yellow]")

        # ---- CALCUL DYNAMIQUE ET AUTOMATIQUE DU CLASSEMENT FINAL ----
        scores = {p: 0.0 for p in tournament.players}

        for r_dict in tournament.rounds:
            r_obj = Round.from_dict(r_dict)
            for m in r_obj.matches:
                if m.player1 in scores:
                    scores[m.player1] += m.score1
                if m.player2 in scores:
                    scores[m.player2] += m.score2

        tournament.results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
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
        console.print(f"[green]Tournoi '{tournament.name}' supprimé avec succès.[/green]")
