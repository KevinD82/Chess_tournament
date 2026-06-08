# controllers/round_controller.py

from database import tournaments_table, TournamentQuery
from models.round import Round
from views.round_view import RoundView


class RoundController:
    """Gère la logique liée aux rounds d'un tournoi (saisie des scores, persistance)."""

    def __init__(self):
        """Initialise le contrôleur des rounds avec sa vue dédiée."""
        self.view = RoundView()

    def enter_results(self, tournament):
        """Permet de définir et d'enregistrer le résultat du dernier round du tournoi."""
        if not tournament.rounds:
            return

        # On récupère le dernier round au format dictionnaire et on l'instancie
        round_obj = Round.from_dict(tournament.rounds[-1])

        # Parcours de tous les matchs du round
        for match in round_obj.matches:
            # Demande le vainqueur (1, N, 2) à la vue
            result = self.view.ask_match_result(match)

            if result is None:
                return

            # Décomposition du tuple de points automatique (1, 0.5 ou 0)
            score1, score2 = result
            match.score1 = score1
            match.score2 = score2

        # On ré-écrase le dernier round mis à jour dans la liste du tournoi
        tournament.rounds[-1] = round_obj.to_dict()

        # Sauvegarde immédiate dans TinyDB
        tournaments_table.update(tournament.to_dict(), TournamentQuery.name == tournament.name)
