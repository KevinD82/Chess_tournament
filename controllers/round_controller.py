# controllers/round_controller.py

from models.round import Round
from models.match import Match
from database import tournaments_table, TournamentQuery
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

        # On prend le dernier round
        round_obj = tournament.rounds[-1]

        # S'il s'agit d'un dictionnaire brut, conversion en objet temporaire
        if isinstance(round_obj, dict):
            round_obj = Round.from_dict(round_obj)
            tournament.rounds[-1] = round_obj

        console.print(f"\n[bold cyan]--- SAISIE DES RÉSULTATS : {round_obj.name} ---[/bold cyan]")

        updated_matches = []

        for match in round_obj.matches:
            # Reconstitution de l'objet Match si nécessaire
            if isinstance(match, dict):
                match_obj = Match(
                    player1=match.get("player1"),
                    score1=float(match.get("score1", 0.0)),
                    player2=match.get("player2"),
                    score2=float(match.get("score2", 0.0))
                )
            else:
                match_obj = match

            # Récupération sécurisée du choix (renvoie obligatoirement '1', '2' ou 'N')
            result = self.view.ask_match_result(match_obj)

            if result == "1":
                match_obj.score1 = 1.0
                match_obj.score2 = 0.0
            elif result == "2":
                match_obj.score1 = 0.0
                match_obj.score2 = 1.0
            elif result == "N":
                match_obj.score1 = 0.5
                match_obj.score2 = 0.5

            # Stockage propre
            match_dict = {
                "player1": match_obj.player1,
                "score1": match_obj.score1,
                "player2": match_obj.player2,
                "score2": match_obj.score2
            }
            updated_matches.append(match_dict)

        # Enregistrement dans l'objet de session
        if isinstance(tournament.rounds[-1], Round):
            tournament.rounds[-1].matches = updated_matches
        else:
            tournament.rounds[-1]["matches"] = updated_matches

        # Sauvegarde TinyDB
        serialized_rounds = []
        for r in tournament.rounds:
            if hasattr(r, "to_dict"):
                serialized_rounds.append(r.to_dict())
            elif isinstance(r, dict):
                serialized_rounds.append(r)

        tournaments_table.update(
            {"rounds": serialized_rounds},
            TournamentQuery.name == tournament.name
        )
