# controllers/player_controller.py

from models.player import Player
from database import players_table, PlayerQuery
from views.player_view import PlayerView
from rich.console import Console

console = Console()


class PlayerController:
    """
    Contrôleur responsable de la gestion des joueurs :
    - création
    - affichage
    - suppression par numéro de liste

    Il utilise PlayerView pour l'affichage et TinyDB pour le stockage.
    """

    def __init__(self):
        self.view = PlayerView()

    # ------------------------------------------------------------------
    # 1. Création d’un joueur
    # ------------------------------------------------------------------
    def create_player(self):
        """
        Demande les informations du joueur via la vue,
        crée un objet Player et l’enregistre dans TinyDB.
        """
        data = self.view.ask_player_info()
        if data is None:
            return

        player = Player(**data)
        players_table.insert(player.to_dict())
        self.view.confirm_player_created(player)

    # ------------------------------------------------------------------
    # 2. Affichage des joueurs
    # ------------------------------------------------------------------
    def list_players(self):
        """Charge tous les joueurs depuis TinyDB et les affiche."""
        records = players_table.all()
        players = [Player.from_dict(r) for r in records]
        self.view.show_players(players)

    # ------------------------------------------------------------------
    # 3. Chargement des joueurs sous forme de dict {id: Player}
    # ------------------------------------------------------------------
    def load_players_lookup(self):
        """Retourne un dict {national_id: Player} pour les contrôleurs."""
        records = players_table.all()
        return {r["national_id"]: Player.from_dict(r) for r in records}

    # ------------------------------------------------------------------
    # 4. Suppression d’un joueur par numéro de liste
    # ------------------------------------------------------------------
    def delete_player(self):
        """
        Affiche la liste des joueurs avec un numéro,
        demande un numéro à supprimer,
        supprime le joueur correspondant dans TinyDB.
        """
        records = players_table.all()
        players = [Player.from_dict(r) for r in records]

        if not players:
            console.print("[red]Aucun joueur enregistré.[/red]")
            return

        # Affichage avec numéros
        self.view.show_players(players)

        raw = self.view.safe_input("Numéro du joueur à supprimer : ")
        if raw is None:
            return

        try:
            index = int(raw) - 1
            player = players[index]
        except (ValueError, IndexError):
            console.print("[red]Numéro invalide.[/red]")
            return

        # Suppression dans TinyDB
        players_table.remove(PlayerQuery.national_id == player.national_id)

        # Confirmation
        self.view.confirm_player_deleted(player)
