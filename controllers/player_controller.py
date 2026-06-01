# controllers/player_controller.py

from models.player import Player
from database import players_table, PlayerQuery
from views.player_view import PlayerView
from rich.console import Console

console = Console()


class PlayerController:
    """
    Contrôleur responsable de :
    - créer un joueur
    - afficher les joueurs
    - supprimer un joueur par numéro
    """

    def __init__(self):
        self.view = PlayerView()

    # --------------------------------------------------------------
    # Création d’un joueur
    # --------------------------------------------------------------
    def create_player(self):
        """
        Demande les informations du joueur via la vue.
        Si l'utilisateur valide, on enregistre dans TinyDB.
        """
        data = self.view.ask_player_info()
        if data is None:
            return  # Annulé

        player = Player(**data)
        players_table.insert(player.to_dict())
        self.view.confirm_player_created(player)

    # --------------------------------------------------------------
    # Affichage des joueurs
    # --------------------------------------------------------------
    def list_players(self):
        """
        Charge tous les joueurs depuis TinyDB et les affiche.
        """
        records = players_table.all()
        players = [Player.from_dict(r) for r in records]
        self.view.show_players(players)

    # --------------------------------------------------------------
    # Suppression d’un joueur par numéro
    # --------------------------------------------------------------
    def delete_player(self):
        """
        Affiche la liste des joueurs avec un numéro.
        L'utilisateur choisit un numéro → suppression dans TinyDB.
        """
        records = players_table.all()
        players = [Player.from_dict(r) for r in records]

        if not players:
            console.print("[red]Aucun joueur enregistré.[/red]")
            return

        # Affichage numéroté
        self.view.show_players(players)

        raw = self.view.safe_input("Numéro du joueur à supprimer : ")
        if raw is None:
            return

        try:
            index = int(raw) - 1
            player = players[index]
        except Exception:
            console.print("[red]Numéro invalide.[/red]")
            return

        # Suppression dans TinyDB
        players_table.remove(PlayerQuery.national_id == player.national_id)

        # Confirmation
        self.view.confirm_player_deleted(player)
