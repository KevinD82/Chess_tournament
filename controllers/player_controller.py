# controllers/player_controller.py

from models.player import Player
from database import players_table
from views.player_view import PlayerView
from tinydb import where
from rich.console import Console

console = Console()


class PlayerController:
    def __init__(self):
        self.view = PlayerView()

    # --------------------------------------------------------------
    # Création d’un joueur
    # --------------------------------------------------------------
    def create_player(self):
        data = self.view.ask_player_info()
        if not data:
            return

        player = Player(**data)
        players_table.insert(player.to_dict())
        console.print("[green]Joueur créé avec succès ![/green]")

    # --------------------------------------------------------------
    # Affichage des joueurs + Option de Modification (Demandée !)
    # --------------------------------------------------------------
    def list_players(self):
        raw_players = players_table.all()
        players = [Player.from_dict(p) for p in raw_players]

        if not self.view.show_players(players):
            return

        # Demande si l'utilisateur veut modifier un joueur affiché
        choice_num = self.view.ask_player_to_edit(len(players))
        if choice_num == 0:
            return

        # Récupération du joueur ciblé et de son doc_id unique TinyDB
        target_index = choice_num - 1
        doc_id_selected = raw_players[target_index].doc_id

        console.print("\n[yellow]📝 Saisie des nouvelles informations :[/yellow]")
        new_data = self.view.ask_player_info()

        if new_data:
            players_table.update(new_data, doc_ids=[doc_id_selected])
            console.print("[green]✓ Le joueur a bien été mis à jour ![/green]")

    # --------------------------------------------------------------
    # Suppression d’un joueur
    # --------------------------------------------------------------
    def delete_player(self):
        players = [Player.from_dict(p) for p in players_table.all()]

        if not players:
            console.print("[yellow]Aucun joueur enregistré.[/yellow]")
            return

        self.view.show_players(players)

        while True:
            choice = console.input("Numéro du joueur à supprimer (Entrée vide = annuler) : ").strip()

            if choice == "":
                console.print("[yellow]Suppression annulée.[/yellow]")
                return

            if not choice.isdigit():
                console.print("[red]Veuillez entrer un numéro valide.[/red]")
                continue

            index = int(choice) - 1

            if index < 0 or index >= len(players):
                console.print("[red]Numéro hors liste.[/red]")
                continue

            player = players[index]
            break

        # Suppression dans TinyDB
        players_table.remove(where("national_id") == player.national_id)
        console.print(f"[green]Joueur {player.first_name} {player.last_name} supprimé.[/green]")
