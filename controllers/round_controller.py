# controllers/round_controller.py

from models.round import Round
from models.match import Match
from database import tournaments_table, TournamentQuery, players_table
from models.player import Player
from views.round_view import RoundView
from rich.console import Console

console = Console()


class RoundController:
    """Gère la saisie des résultats et la mise à jour des scores d'un round."""

    def __init__(self):
        """Initialise le contrôleur de round avec sa vue."""
        self.view = RoundView()

    def enter_results(self, tournament):
        """Permet à l'utilisateur de saisir le résultat de chaque match du round en cours."""
        if not tournament.rounds:
            console.print("[yellow]Aucun round disponible pour ce tournoi.[/yellow]")
            return

        # Construction du dictionnaire des joueurs pour permettre à la vue d'afficher les noms complets
        players_dict = {p['national_id']: Player.from_dict(p) for p in players_table.all()}

        # On cible le dernier round généré en mémoire vive
        round_obj = tournament.rounds[-1]

        # Si le round est un dictionnaire brut issu de TinyDB, on le convertit en objet
        if isinstance(round_obj, dict):
            round_obj = Round.from_dict(round_obj)
            tournament.rounds[-1] = round_obj

        console.print(f"\n[bold cyan]--- SAISIE DES RÉSULTATS : {round_obj.name} ---[/bold cyan]")

        updated_matches = []

        # Parcours et traitement de chaque match du round
        for match in round_obj.matches:
            if isinstance(match, dict):
                match_obj = Match(
                    player1=match.get("player1"),
                    score1=float(match.get("score1", 0.0)),
                    player2=match.get("player2"),
                    score2=float(match.get("score2", 0.0))
                )
            else:
                match_obj = match

            # Appel de la vue en transmettant le dictionnaire des joueurs pour l'affichage textuel complet
            result = self.view.ask_match_result(match_obj, players_dict=players_dict)

            # Assignation stricte des scores selon le choix validé
            if result == "1":
                match_obj.score1 = 1.0
                match_obj.score2 = 0.0
            elif result == "2":
                match_obj.score1 = 0.0
                match_obj.score2 = 1.0
            elif result == "N":
                match_obj.score1 = 0.5
                match_obj.score2 = 0.5

            # Structuration en dictionnaire propre pour la sauvegarde
            match_dict = {
                "player1": match_obj.player1,
                "score1": match_obj.score1,
                "player2": match_obj.player2,
                "score2": match_obj.score2
            }
            updated_matches.append(match_dict)

        # Enregistrement des matchs mis à jour dans l'arborescence du tournoi actif
        if isinstance(tournament.rounds[-1], Round):
            tournament.rounds[-1].matches = updated_matches
        else:
            tournament.rounds[-1]["matches"] = updated_matches

        # Sérialisation globale propre de tous les rounds pour TinyDB
        serialized_rounds = []
        for r in tournament.rounds:
            if hasattr(r, "to_dict"):
                serialized_rounds.append(r.to_dict())
            elif isinstance(r, dict):
                serialized_rounds.append(r)

        # Mise à jour immédiate et persistante de la base de données
        tournaments_table.update(
            {"rounds": serialized_rounds},
            TournamentQuery.name == tournament.name
        )
