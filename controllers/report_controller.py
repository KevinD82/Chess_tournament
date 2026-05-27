# controllers/report_controller.py

# Importation des tables TinyDB et de la requête pour filtrer les tournois
from database import players_table, tournaments_table, TournamentQuery

# Importation des modèles pour reconstruire les objets Python depuis TinyDB
from models.player import Player
from models.tournament import Tournament

# Importation de la vue dédiée aux rapports
from views.report_view import ReportView

# Importation du PlayerController pour reconstruire les joueurs depuis la base
from controllers.player_controller import PlayerController


class ReportController:
    """
    Le ReportController gère toutes les fonctionnalités liées aux rapports :
    - liste des joueurs
    - liste des tournois
    - détails d’un tournoi
    - rounds d’un tournoi
    - matchs d’un tournoi
    - scores finaux
    - historique complet

    Il ne modifie jamais les données : il ne fait qu'afficher.
    """

    def __init__(self):
        # Vue utilisée pour afficher les rapports
        self.view = ReportView()

        # On utilise PlayerController pour reconstruire les joueurs depuis TinyDB
        self.player_controller = PlayerController()

    # ----------------------------------------------------------------------
    # 1. Liste de tous les joueurs
    # ----------------------------------------------------------------------
    def list_all_players(self):
        """
        Récupère tous les joueurs dans TinyDB,
        les convertit en objets Player,
        puis les affiche via la vue.
        """
        records = players_table.all()
        players = [Player.from_dict(r) for r in records]
        self.view.show_players(players)

    # ----------------------------------------------------------------------
    # 2. Liste de tous les tournois
    # ----------------------------------------------------------------------
    def list_all_tournaments(self):
        """
        Récupère tous les tournois dans TinyDB.
        Pour chaque tournoi, on reconstruit les objets Player associés
        grâce au lookup fourni par PlayerController.
        """
        records = tournaments_table.all()
        players_lookup = self.player_controller.load_players_lookup()

        tournaments = [
            Tournament.from_dict(r, players_lookup)
            for r in records
        ]

        self.view.show_tournaments(tournaments)

    # ----------------------------------------------------------------------
    # Méthode interne pour charger un tournoi demandé par l'utilisateur
    # ----------------------------------------------------------------------
    def _load_tournament(self):
        """
        Demande à l'utilisateur le nom d'un tournoi.
        Si l'utilisateur annule → retourne None.
        Si le tournoi n'existe pas → affiche une erreur et retourne None.
        Sinon → retourne un objet Tournament complet.
        """
        name = self.view.ask_tournament_name()

        # Annulation utilisateur
        if name is None:
            return None

        # Recherche du tournoi dans TinyDB
        record = tournaments_table.get(TournamentQuery.name == name)

        if not record:
            self.view.error_not_found()
            return None

        # Reconstruction des joueurs du tournoi
        players_lookup = self.player_controller.load_players_lookup()

        return Tournament.from_dict(record, players_lookup)

    # ----------------------------------------------------------------------
    # 3. Détails d’un tournoi
    # ----------------------------------------------------------------------
    def tournament_details(self):
        """
        Affiche les informations générales d’un tournoi :
        - nom
        - lieu
        - dates
        - description
        """
        t = self._load_tournament()
        if t:
            self.view.show_tournament_details(t)

    # ----------------------------------------------------------------------
    # 4. Rounds d’un tournoi
    # ----------------------------------------------------------------------
    def tournament_rounds(self):
        """
        Affiche la liste des rounds d’un tournoi :
        - nom du round
        - heure de début
        - heure de fin
        """
        t = self._load_tournament()
        if t:
            self.view.show_rounds(t.rounds)

    # ----------------------------------------------------------------------
    # 5. Matchs d’un tournoi
    # ----------------------------------------------------------------------
    def tournament_matches(self):
        """
        Affiche tous les matchs d’un tournoi, round par round :
        - joueur 1
        - score
        - joueur 2
        - score
        """
        t = self._load_tournament()
        if t:
            self.view.show_matches(t.rounds)

    # ----------------------------------------------------------------------
    # 6. Scores finaux d’un tournoi
    # ----------------------------------------------------------------------
    def tournament_scores(self):
        """
        Affiche le classement final d’un tournoi :
        - joueurs triés par score décroissant
        """
        t = self._load_tournament()
        if t:
            self.view.show_final_scores(t.players)

    # ----------------------------------------------------------------------
    # 7. Historique complet d’un tournoi
    # ----------------------------------------------------------------------
    def full_history(self):
        """
        Affiche l’historique complet d’un tournoi :
        - détails du tournoi
        - rounds
        - matchs
        - scores finaux

        C’est le rapport le plus complet.
        """
        t = self._load_tournament()
        if t:
            self.view.show_full_history(t)
