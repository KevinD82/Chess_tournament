# controllers/player_controller.py

# Importation du modèle Player, qui représente un joueur dans l'application.
from models.player import Player

# Importation de la table TinyDB contenant les joueurs.
from database import players_table

# Importation de la vue dédiée aux interactions utilisateur concernant les joueurs.
from views.player_view import PlayerView


class PlayerController:
    """
    Le PlayerController gère toute la logique métier liée aux joueurs :
    - création d'un joueur
    - affichage de la liste des joueurs
    - chargement des joueurs pour d'autres contrôleurs (tournois, rapports)
    """

    def __init__(self):
        # La vue associée à ce contrôleur (affichage + saisies utilisateur)
        self.view = PlayerView()

    def create_player(self):
        """
        Demande à la vue les informations nécessaires pour créer un joueur.
        Si l'utilisateur annule (via 'echap', 'annuler', etc.), la vue renvoie None.
        Dans ce cas, on retourne simplement au menu sans rien faire.
        """
        data = self.view.ask_player_info()

        # Annulation utilisateur → retour au menu
        if data is None:
            return

        # Création d'un objet Player à partir des données saisies
        player = Player(**data)

        # Sauvegarde dans la base TinyDB
        players_table.insert(player.to_dict())

        # Confirmation visuelle
        self.view.confirm_player_created(player)

    def list_players(self):
        """
        Récupère tous les joueurs enregistrés dans TinyDB,
        les convertit en objets Player,
        puis les affiche via la vue.
        """
        records = players_table.all()

        # Conversion des dictionnaires TinyDB → objets Player
        players = [Player.from_dict(r) for r in records]

        # Affichage via la vue
        self.view.show_players(players)

    def load_players_lookup(self):
        """
        Charge tous les joueurs et retourne un dictionnaire
        permettant de retrouver un joueur à partir de son identifiant national.

        Ce lookup est utilisé par :
        - TournamentController (pour reconstruire les joueurs d’un tournoi)
        - ReportController (pour afficher les rapports)
        """
        records = players_table.all()

        # On crée un dictionnaire : { national_id : Player }
        return {r["national_id"]: Player.from_dict(r) for r in records}
