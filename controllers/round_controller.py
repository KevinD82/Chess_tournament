# controllers/round_controller.py

# Importation de la base de données TinyDB et de la requête permettant
# de cibler un tournoi spécifique pour mise à jour.
from database import tournaments_table, TournamentQuery

# Importation du modèle Round, qui gère la logique métier d’un round :
# création, génération des matchs, structure interne, etc.
from models.round import Round

# Importation de la vue dédiée aux rounds (affichage + saisie des scores)
from views.round_view import RoundView


class RoundController:
    """
    Le RoundController gère toute la logique liée aux rounds d’un tournoi :
    - création d’un nouveau round
    - saisie des résultats des matchs
    - mise à jour du tournoi dans la base de données

    Il ne gère pas l’affichage global du tournoi, uniquement les rounds.
    """

    def __init__(self):
        # Vue utilisée pour afficher les informations et demander les scores
        self.view = RoundView()

    # ----------------------------------------------------------------------
    # 1. Création d’un nouveau round
    # ----------------------------------------------------------------------
    def create_round(self, tournament):
        """
        Crée un nouveau round pour le tournoi donné.
        - Round.create_new(tournament) génère automatiquement :
            * le nom du round (Round 1, Round 2…)
            * les matchs selon l’algorithme suisse
            * l’heure de début
        - Le round est ajouté à la liste des rounds du tournoi
        - Le tournoi est sauvegardé dans TinyDB
        - La vue affiche un message de confirmation
        """

        # Création du round via la logique métier du modèle Round
        round_obj = Round.create_new(tournament)

        # Ajout du round au tournoi
        tournament.rounds.append(round_obj)

        # Mise à jour du tournoi dans la base TinyDB
        tournaments_table.update(
            tournament.to_dict(),
            TournamentQuery.name == tournament.name
        )

        # Affichage d’un message de confirmation
        self.view.show_round(round_obj)

    # ----------------------------------------------------------------------
    # 2. Saisie des résultats d’un round
    # ----------------------------------------------------------------------
    def enter_results(self, tournament):
        """
        Permet de saisir les résultats du dernier round du tournoi.
        - Si aucun round n’existe → rien à faire
        - Pour chaque match :
            * la vue demande les scores
            * si l’utilisateur annule → retour immédiat
        - Les scores sont enregistrés dans les objets Match
        - Le tournoi est sauvegardé dans TinyDB
        """

        # Si le tournoi n’a aucun round, on ne peut rien saisir
        if not tournament.rounds:
            return

        # On récupère le dernier round (celui en cours)
        round_obj = tournament.rounds[-1]

        # Parcours de tous les matchs du round
        for match in round_obj.matches:

            # Demande des scores via la vue
            result = self.view.ask_match_result(match)

            # Annulation utilisateur → retour sans sauvegarder
            if result is None:
                return

            # Décomposition du tuple (score1, score2)
            score1, score2 = result

            # Mise à jour des scores dans l’objet Match
            match.score1 = score1
            match.score2 = score2

        # Sauvegarde du tournoi mis à jour dans TinyDB
        tournaments_table.update(
            tournament.to_dict(),
            TournamentQuery.name == tournament.name
        )

        # Confirmation visuelle
        self.view.confirm_results_saved()
