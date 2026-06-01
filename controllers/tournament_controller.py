# controllers/tournament_controller.py

from models.tournament import Tournament
from models.round import Round
from models.match import Match
from models.player import Player

from database import tournaments_table, TournamentQuery
from views.tournament_view import TournamentView
from views.round_view import RoundView
from rich.console import Console

console = Console()


class TournamentController:
    """
    Contrôleur responsable de :
    - créer un tournoi
    - lister les tournois
    - gérer un tournoi (rounds, matchs, scores)
    """

    def __init__(self):
        self.view = TournamentView()
        self.round_view = RoundView()

    # --------------------------------------------------------------
    # Création d’un tournoi
    # --------------------------------------------------------------
    def create_tournament(self):
        data = self.view.ask_tournament_info()
        if data is None:
            return

        tournament = Tournament(**data)
        tournaments_table.insert(tournament.to_dict())

        console.print(f"[green]Tournoi '{tournament.name}' créé avec succès ![/green]")

    # --------------------------------------------------------------
    # Liste des tournois
    # --------------------------------------------------------------
    def list_tournaments(self):
        records = tournaments_table.all()
        tournaments = [Tournament.from_dict(r) for r in records]

        if not tournaments:
            console.print("[red]Aucun tournoi enregistré.[/red]")
            return

        for t in tournaments:
            console.print(f"- {t.name} ({t.location}) du {t.start_date} au {t.end_date}")

    # --------------------------------------------------------------
    # Gestion d’un tournoi
    # --------------------------------------------------------------
    def manage_tournament(self):
        records = tournaments_table.all()
        tournaments = [Tournament.from_dict(r) for r in records]

        if not tournaments:
            console.print("[red]Aucun tournoi disponible.[/red]")
            return

        # Affichage numéroté
        for i, t in enumerate(tournaments, start=1):
            console.print(f"{i}. {t.name} ({t.location})")

        raw = console.input("Numéro du tournoi à gérer : ")
        try:
            index = int(raw) - 1
            tournament = tournaments[index]
        except:
            console.print("[red]Numéro invalide.[/red]")
            return

        self.manage_selected_tournament(tournament)

    # --------------------------------------------------------------
    # Menu interne d’un tournoi
    # --------------------------------------------------------------
    def manage_selected_tournament(self, tournament):
        while True:
            console.print(f"\n[bold cyan]Gestion du tournoi : {tournament.name}[/bold cyan]")
            console.print("1. Ajouter des joueurs")
            console.print("2. Lancer un round")
            console.print("3. Voir les rounds")
            console.print("0. Retour\n")

            choice = console.input("Votre choix : ")

            if choice == "1":
                self.add_players_to_tournament(tournament)

            elif choice == "2":
                self.start_round(tournament)

            elif choice == "3":
                self.show_rounds(tournament)

            elif choice == "0":
                return

    # --------------------------------------------------------------
    # Ajouter des joueurs
    # --------------------------------------------------------------
    def add_players_to_tournament(self, tournament):
        from database import players_table
        players = [Player.from_dict(r) for r in players_table.all()]

        selected = self.view.select_players(players)
        if selected is None:
            return

        tournament.players = [p.national_id for p in selected]
        self._save_tournament(tournament)

        console.print("[green]Joueurs ajoutés au tournoi ![/green]")

    # --------------------------------------------------------------
    # Lancer un round
    # --------------------------------------------------------------
    def start_round(self, tournament):
        if not tournament.players:
            console.print("[red]Aucun joueur dans ce tournoi.[/red]")
            return

        round_number = len(tournament.rounds) + 1
        round_obj = Round(name=f"Round {round_number}")

        # Création des matchs (pairing simple)
        players = tournament.players.copy()
        if len(players) % 2 != 0:
            console.print("[red]Nombre impair de joueurs ![/red]")
            return

        matches = []
        for i in range(0, len(players), 2):
            p1 = players[i]
            p2 = players[i + 1]
            matches.append(Match(player1=p1, player2=p2))

        round_obj.matches = matches

        # Saisie des scores
        for match in round_obj.matches:
            score = self.round_view.ask_match_result(match)
            if score is None:
                return
            match.score1, match.score2 = score

        tournament.rounds.append(round_obj)
        self._save_tournament(tournament)

        console.print("[green]Round terminé et enregistré ![/green]")

    # --------------------------------------------------------------
    # Affichage des rounds
    # --------------------------------------------------------------
    def show_rounds(self, tournament):
        if not tournament.rounds:
            console.print("[yellow]Aucun round enregistré.[/yellow]")
            return

        for r in tournament.rounds:
            console.print(f"[cyan]{r.name}[/cyan]")
            for m in r.matches:
                console.print(f"- {m.player1} {m.score1} vs {m.player2} {m.score2}")

    # --------------------------------------------------------------
    # Sauvegarde
    # --------------------------------------------------------------
    def _save_tournament(self, tournament):
        tournaments_table.update(
            tournament.to_dict(),
            TournamentQuery.name == tournament.name
        )
