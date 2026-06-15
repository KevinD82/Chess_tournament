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

    def create_tournament(self):
        data = self.view.ask_tournament_info()
        if not data:
            return

        # On crée le tournoi sans joueurs au départ
        tournament = Tournament(**data)
        tournaments_table.insert(tournament.to_dict())
        console.print("[green]Tournoi créé avec succès ![/green]")

    def list_tournaments(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        self.view.show_tournaments(tournaments)

    def add_players_to_tournament(self):
        """Permet de sélectionner les joueurs participants à un tournoi (ex : 4 sur 100)."""
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        if not tournaments:
            console.print("[yellow]Aucun tournoi disponible.[/yellow]")
            return

        # Sélection du tournoi
        selected_tournament = self.view.select_tournament(tournaments)
        if not selected_tournament:
            console.print("[red]Sélection de tournoi invalide.[/red]")
            return

        # Récupération de tous les joueurs du club
        all_players = players_table.all()
        if not all_players:
            console.print("[yellow]Aucun joueur enregistré.[/yellow]")
            return

        # Sélection des joueurs participants
        selected_players = self.view.select_players(all_players)
        if len(selected_players) != 4:
            console.print("[red]Vous devez sélectionner exactement 4 joueurs.[/red]")
            return

        # On stocke les national_id des joueurs dans le tournoi
        player_ids = [p["national_id"] for p in selected_players]

        tournaments_table.update(
            {"players": player_ids},
            TournamentQuery.name == selected_tournament.name
        )

        console.print("[green]Les joueurs ont été ajoutés au tournoi.[/green]")

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

    def next_round(self, tournament):
        """Génère le prochain round en utilisant UNIQUEMENT les joueurs sélectionnés pour ce tournoi."""
        total_rounds = getattr(tournament, "number_of_rounds", getattr(tournament, "num_rounds", 3))

        # Vérification que le round précédent a bien des scores
        if tournament.rounds:
            last_round = tournament.rounds[-1]

            if isinstance(last_round, dict):
                matches_to_check = last_round.get('matches', [])
            else:
                matches_to_check = getattr(last_round, 'matches', [])

            for match in matches_to_check:
                if hasattr(match, "score1"):
                    s1, s2 = match.score1, match.score2
                elif isinstance(match, dict):
                    s1 = match.get("score1", match.get("score_j1", match.get("score_player1", 0.0)))
                    s2 = match.get("score2", match.get("score_j2", match.get("score_player2", 0.0)))
                else:
                    try:
                        s1, s2 = match[0][1], match[1][1]
                    except (IndexError, TypeError):
                        s1, s2 = 0.0, 0.0

                try:
                    val1 = float(s1) if s1 is not None else 0.0
                    val2 = float(s2) if s2 is not None else 0.0
                except (ValueError, TypeError):
                    val1, val2 = 0.0, 0.0

                if val1 == 0.0 and val2 == 0.0:
                    console.print("[red]⚠️ Impossible de lancer un nouveau round ![/red]")
                    console.print("[red]Vous devez d'abord saisir les résultats du round en cours (Option 2).[/red]")
                    return

        if len(tournament.rounds) >= total_rounds:
            console.print("[yellow]Ce tournoi est déjà terminé (tous les rounds ont été joués).[/yellow]")
            return

        # NOUVELLE RÈGLE : on utilise uniquement les joueurs du tournoi
        if not getattr(tournament, "players", []):
            console.print("[red]Aucun joueur sélectionné pour ce tournoi.[/red]")
            console.print("[yellow]Utilisez l'option 'Ajouter des joueurs au tournoi' avant de générer un round.[/yellow]")
            return

        # Récupération des joueurs à partir de leurs national_id
        players_data = []
        for nat_id in tournament.players:
            p = players_table.get(where("national_id") == nat_id)
            if p:
                players_data.append(p)

        if len(players_data) < 2:
            console.print("[red]Erreur : Il n'y a pas assez de joueurs sélectionnés pour ce tournoi.[/red]")
            return

        round_number = len(tournament.rounds) + 1
        console.print(f"\n[green]Génération du Round {round_number}...[/green]")

        matches_objects = []
        random.shuffle(players_data)

        for i in range(0, len(players_data) - 1, 2):
            p1 = players_data[i]
            p2 = players_data[i + 1]

            match_obj = Match(
                player1=p1['national_id'],
                score1=0.0,
                player2=p2['national_id'],
                score2=0.0
            )
            matches_objects.append(match_obj)

        current_now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        new_round_obj = Round(
            name=f"Round {round_number}",
            matches=matches_objects,
            start_time=current_now_str,
            end_time=""
        )

        tournament.rounds.append(new_round_obj)

        tournaments_table.update(
            {
                "rounds": [
                    r.to_dict() if hasattr(r, "to_dict") else r
                    for r in tournament.rounds
                ]
            },
            TournamentQuery.name == tournament.name
        )

        console.print(f"[green]Le {new_round_obj.name} a été généré à {current_now_str} ![/green]")

    def play_round_scores(self, tournament):
        if not tournament.rounds:
            console.print("[yellow]Aucun round n'a encore été généré pour ce tournoi.[/yellow]")
            return

        self.round_controller.enter_results(tournament)
        console.print("[green]Scores du round enregistrés ![/green]")

    def delete_tournament(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        self.view.show_tournaments(tournaments)
        choice = console.input("Numéro du tournoi à supprimer : ").strip()

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(tournaments):
            console.print("[red]Numéro invalide.[/red]")
            return

        tournament = tournaments[int(choice) - 1]
        tournaments_table.remove(TournamentQuery.name == tournament.name)
        console.print(f"[green]Tournoi '{tournament.name}' supprimé.[/green]")
