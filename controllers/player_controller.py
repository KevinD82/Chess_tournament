# controllers/player_controller.py

from models.player import Player
from models.tournament import Tournament
from database import players_table, tournaments_table
from views.player_view import PlayerView
from tinydb import where
from rich.console import Console

console = Console()


class PlayerController:
    """Logique métier liée aux joueurs."""

    def __init__(self):
        self.view = PlayerView()

    def create_player(self):
<<<<<<< HEAD
        """Création d'un joueur avec affichage préalable complet de la base."""
        console.print("\n[bold magenta]=== BASE DE DONNÉES DES JOUEURS ACTUELS ===[/bold magenta]")
        # Affiche le tableau Rich complet (N°, ID, Nom, Prénom, Naissance, Statut)
        self.list_players()

        # Déclenche ensuite le questionnaire de création
=======
        # Afficher les joueurs existants pour éviter les doublons
        existing_players = [Player.from_dict(p) for p in players_table.all()]
        if existing_players:
            console.print("\n[bold cyan]Joueurs existants :[/bold cyan]")
            self.view.show_players(existing_players)

>>>>>>> 1511e2a3c98dd82fcb10c2c42a980ae48edac3ad
        data = self.view.ask_player_info()
        if not data:
            return

<<<<<<< HEAD
        # Sécurité stricte doublon ID
        existing_players = players_table.search(where("national_id") == data["national_id"])
        if existing_players:
            console.print(
                f"\n[bold red]Erreur : Un joueur avec l'ID National '{data['national_id']}' "
                f"existe déjà dans votre base de données ![/bold red]"
            )
            return
=======
        # Vérification doublon par national_id
        for p in existing_players:
            if p.national_id == data["national_id"]:
                console.print("[red]Un joueur avec ce National ID existe déjà ![/red]")
                return
>>>>>>> 1511e2a3c98dd82fcb10c2c42a980ae48edac3ad

        player = Player(**data)
        players_table.insert(player.to_dict())
        console.print("[green]Joueur créé avec succès ![/green]")

    def list_players(self):
        """Affiche la liste de tous les joueurs via la vue dédiée."""
        players = [Player.from_dict(p) for p in players_table.all()]
        self.view.show_players(players)

    def delete_player(self):
        """Désactive ou supprime un joueur selon son statut dans les tournois."""
        players = [Player.from_dict(p) for p in players_table.all()]

        if not players:
            console.print("[yellow]Aucun joueur enregistré.[/yellow]")
            return

        self.view.show_players(players)

        while True:
            choice = console.input("Numéro du joueur à désactiver/supprimer (Entrée vide = annuler) : ").strip()

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

<<<<<<< HEAD
        # Vérification des tournois en cours
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        
        is_in_ongoing_tournament = False
        associated_tournament_name = ""

        for t in tournaments:
            if player.national_id in t.players:
                if len(t.rounds) < t.number_of_rounds:
                    is_in_ongoing_tournament = True
                    associated_tournament_name = t.name
                    break

        if is_in_ongoing_tournament:
            console.print(
                f"[bold red]Action impossible :[/bold red] Le joueur {player.first_name} {player.last_name} "
                f"est inscrit dans le tournoi [bold yellow]'{associated_tournament_name}'[/bold yellow] "
                f"qui est toujours en cours."
            )
            return

        # Gestion de l'historique passé vs suppression définitive
        is_in_past_tournament = any(player.national_id in t.players for t in tournaments)

        if is_in_past_tournament:
            players_table.update(
                {"is_active": False},
                where("national_id") == player.national_id
            )
            console.print(f"[green]Le joueur {player.first_name} {player.last_name} est désormais [red]Inactif[/red].[/green]")
        else:
            players_table.remove(where("national_id") == player.national_id)
            console.print(f"[green]Le joueur {player.first_name} {player.last_name} a été supprimé de la base.[/green]")
=======
        # Vérifier si le joueur participe à un tournoi
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        for t in tournaments:
            if player.national_id in getattr(t, "players", []):
                console.print("[red]Impossible de supprimer ce joueur : il participe à un tournoi.[/red]")
                console.print(f"[yellow]Tournoi concerné : {t.name}[/yellow]")
                return

        players_table.remove(where("national_id") == player.national_id)
        console.print(f"[green]Joueur {player.first_name} {player.last_name} supprimé avec succès ![/green]")
>>>>>>> 1511e2a3c98dd82fcb10c2c42a980ae48edac3ad
