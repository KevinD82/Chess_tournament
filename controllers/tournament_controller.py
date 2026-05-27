# controllers/tournament_controller.py

# Importation du modèle Tournament, qui contient toute la logique métier
# d’un tournoi : joueurs, rounds, reconstruction depuis TinyDB, etc.
from models.tournament import Tournament

# Importation de la base TinyDB et de la requête permettant de cibler un tournoi
from database import tournaments_table, TournamentQuery

# Importation de la vue dédiée aux tournois (affichage + saisies)
from views.tournament_view import TournamentView

# Importation du PlayerController pour charger les joueurs depuis la base
from controllers.player_controller import PlayerController

# Importation du RoundController pour gérer les rounds et les résultats
from controllers.round_controller import RoundController


class TournamentController:
    """
    Le TournamentController gère toute la logique métier liée aux tournois :
    - création d’un tournoi
    - sélection des joueurs
    - affichage de la liste des tournois
    - gestion d’un tournoi existant (rounds, résultats)
    """

    def __init__(self):
        # Vue utilisée pour afficher les informations et demander les saisies
        self.view = TournamentView()

        # Contrôleur des joueurs (pour charger les joueurs depuis TinyDB)
        self.player_controller = PlayerController()

        # Contrôleur des rounds (création + saisie des résultats)
        self.round_controller = RoundController()

    # ----------------------------------------------------------------------
    # 1. Création d’un tournoi
    # ----------------------------------------------------------------------
    def create_tournament(self):
        """
        Demande les informations du tournoi via la vue.
        Si l’utilisateur annule → retour au menu.
        Ensuite, demande la sélection des joueurs.
        Enfin, crée et sauvegarde le tournoi dans TinyDB.
        """

        # Demande des infos générales du tournoi
        data = self.view.ask_tournament_info()
        if data is None:
            return  # Annulation utilisateur

        # Chargement de tous les joueurs existants
        players = self.player_controller.load_players_lookup().values()

        # Sélection des joueurs participant au tournoi
        selected = self.view.select_players(list(players))
        if selected is None:
            return  # Annulation utilisateur

        # Création de l'objet Tournament
        tournament = Tournament(**data, players=selected)

        # Sauvegarde dans TinyDB
        tournaments_table.insert(tournament.to_dict())

        # Confirmation visuelle
        self.view.confirm_tournament_created(tournament)

    # ----------------------------------------------------------------------
    # 2. Liste des tournois
    # ----------------------------------------------------------------------
    def list_tournaments(self):
        """
        Récupère tous les tournois depuis TinyDB,
        reconstruit les objets Tournament,
        puis les affiche via la vue.
        """

        records = tournaments_table.all()

        # Lookup des joueurs pour reconstruire les objets Player
        players_lookup = self.player_controller.load_players_lookup()

        # Reconstruction des tournois
        tournaments = [
            Tournament.from_dict(r, players_lookup)
            for r in records
        ]

        # Affichage
        self.view.show_tournaments(tournaments)

    # ----------------------------------------------------------------------
    # 3. Gestion d’un tournoi existant
    # ----------------------------------------------------------------------
    def manage_tournament(self):
        """
        Permet de gérer un tournoi existant :
        - créer un round
        - saisir les résultats
        - afficher les informations
        """

        # Demande du nom du tournoi à gérer
        name = self.view.ask_tournament_name()
        if name is None:
            return  # Annulation utilisateur

        # Recherche du tournoi dans TinyDB
        record = tournaments_table.get(TournamentQuery.name == name)
        if not record:
            self.view.error_not_found()
            return

        # Reconstruction des joueurs du tournoi
        players_lookup = self.player_controller.load_players_lookup()

        # Reconstruction de l'objet Tournament complet
        tournament = Tournament.from_dict(record, players_lookup)

        # Boucle de gestion du tournoi
        while True:
            choice = self.view.tournament_menu(tournament)

            # Annulation utilisateur → retour au menu principal
            if choice is None:
                return

            # 1. Créer un nouveau round
            if choice == "1":
                self.round_controller.create_round(tournament)

            # 2. Saisir les résultats du round en cours
            elif choice == "2":
                self.round_controller.enter_results(tournament)

            # 0. Retour au menu principal
            elif choice == "0":
                return
