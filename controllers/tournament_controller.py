import random
from datetime import datetime
from tinydb import where
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from database import tournaments_table, players_table, TournamentQuery
from views.tournament_view import TournamentView
from controllers.round_controller import RoundController
from rich.console import Console

console = Console()


class TournamentController:
    """Logique métier des tournois : création, sélection des joueurs, rounds, blocages."""

    def __init__(self):
        self.view = TournamentView()
        self.round_controller = RoundController()

    # ---------------------------------------------------------
    # CRÉATION
    # ---------------------------------------------------------
    def create_tournament(self):
        data = self.view.ask_tournament_info()
        if not data:
            return

        tournament = Tournament(**data)
        tournaments_table.insert(tournament.to_dict())
        console.print("[green]Tournoi créé avec succès ![/green]")

    # ---------------------------------------------------------
    # LISTE
    # ---------------------------------------------------------
    def list_tournaments(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        self.view.show_tournaments(tournaments)

    # ---------------------------------------------------------
    # AJOUT DES JOUEURS
    # ---------------------------------------------------------
    def add_players_to_tournament(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        if not tournaments:
            console.print("[yellow]Aucun tournoi disponible.[/yellow]")
            return

        selected_tournament = self.view.select_tournament(tournaments)
        if not selected_tournament:
            console.print("[red]Sélection de tournoi invalide.[/red]")
            return

        all_players = players_table.all()
        if not all_players:
            console.print("[yellow]Aucun joueur enregistré.[/yellow]")
            return

        selected_players = self.view.select_players(all_players)
        if len(selected_players) != 4:
            console.print("[red]Vous devez sélectionner exactement 4 joueurs.[/red]")
            return

        player_ids = [p["national_id"] for p in selected_players]

        tournaments_table.update(
            {"players": player_ids},
            TournamentQuery.name == selected_tournament.name
        )

        console.print("[green]Les joueurs ont été ajoutés au tournoi.[/green]")

    # ---------------------------------------------------------
    # MENU PILOTAGE
    # ---------------------------------------------------------
    def manage_tournament(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        if not tournaments:
            console.print("[yellow]Aucun tournoi disponible.[/yellow]")
            return

        self.view.show_tournaments(tournaments)
        choice = console.input("\nSélectionnez le numéro du tournoi à piloter : ").strip()

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(tournaments):
            console.print("[red]Numéro invalide.[/red]")
            return

        selected_tournament_name = tournaments[int(choice) - 1].name

        while True:
            db_data = tournaments_table.get(TournamentQuery.name == selected_tournament_name)
            if not db_data:
                console.print("[red]Erreur : Le tournoi est introuvable en base.[/red]")
                break

            tournament = Tournament.from_dict(db_data)

            console.print(f"\n[bold magenta]--- MENU PILOTAGE : {tournament.name} ---[/bold magenta]")
            console.print("1. Générer et lancer le prochain round")
            console.print("2. Saisir les résultats du round actuel")
            console.print("0. Retour")

            sub_choice = console.input("\n[bold yellow]Votre choix : [/bold yellow]").strip()

            if sub_choice == "1":
                self.next_round(tournament)
            elif sub_choice == "2":
                self.play_round_scores(tournament)
            elif sub_choice == "0":
                break
            else:
                console.print("[red]Choix invalide.[/red]")

    # ---------------------------------------------------------
    # GÉNÉRATION DU ROUND
    # ---------------------------------------------------------
    def next_round(self, tournament):
        total_rounds = getattr(tournament, "number_of_rounds", 3)

        # Vérifier si le round précédent est complété
        if tournament.rounds:
            last_round = tournament.rounds[-1]

            for match in last_round.matches:

                # Gestion dict OU objet Match
                if isinstance(match, dict):
                    s1 = match.get("score1", 0.0)
                    s2 = match.get("score2", 0.0)
                else:
                    s1 = match.score1
                    s2 = match.score2

                if float(s1) == 0.0 and float(s2) == 0.0:
                    console.print("[red]⚠️ Saisir les scores avant de générer un nouveau round.[/red]")
                    return

        # Vérifier nombre de rounds
        if len(tournament.rounds) >= total_rounds:
            console.print("[yellow]Tous les rounds ont déjà été joués.[/yellow]")
            return

        # Vérifier joueurs sélectionnés
        if not getattr(tournament, "players", []):
            console.print("[red]Aucun joueur sélectionné pour ce tournoi.[/red]")
            return

        # Charger les joueurs depuis la base
        players_data = []
        for nat_id in tournament.players:
            p = players_table.get(where("national_id") == nat_id)
            if p:
                players_data.append(p)

        random.shuffle(players_data)

        # Génération des matchs
        matches = []
        for i in range(0, len(players_data) - 1, 2):
            p1 = players_data[i]
            p2 = players_data[i + 1]

            matches.append(
                Match(
                    player1=p1["national_id"],
                    score1=0.0,
                    player2=p2["national_id"],
                    score2=0.0
                )
            )

        round_number = len(tournament.rounds) + 1
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        new_round = Round(
            name=f"Round {round_number}",
            matches=matches,
            start_time=now,
            end_time=""
        )

        tournament.rounds.append(new_round)

        # Sauvegarde en base
        tournaments_table.update(
            {"rounds": [r.to_dict() for r in tournament.rounds]},
            TournamentQuery.name == tournament.name
        )

        console.print(f"[green]Round {round_number} généré avec succès ![/green]")

    # ---------------------------------------------------------
    # SAISIE DES SCORES
    # ---------------------------------------------------------
    def play_round_scores(self, tournament):
        if not tournament.rounds:
            console.print("[yellow]Aucun round n'a encore été généré.[/yellow]")
            return

        self.round_controller.enter_results(tournament)
        console.print("[green]Scores enregistrés ![/green]")
