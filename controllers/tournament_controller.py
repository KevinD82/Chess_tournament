# controllers/tournament_controller.py

from rich.console import Console
from rich.panel import Panel

from models.tournament import Tournament
from models.round import Round
from models.match import Match
from controllers.player_controller import PlayerController
from views.tournament_view import TournamentView
from views.round_view import RoundView
from database import tournaments_table, TournamentQuery

console = Console()


class TournamentController:
    def __init__(self):
        self.view = TournamentView()
        self.round_view = RoundView()

    # --------------------------------------------------------------
    # Création d’un tournoi
    # --------------------------------------------------------------
    def create_tournament(self):
        data = self.view.ask_tournament_info()
        if not data:
            return

        tournament = Tournament(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            description=data["description"],
        )

        tournaments_table.insert(tournament.to_dict())
        console.print("[green]Tournoi créé avec succès ![/green]")

    # --------------------------------------------------------------
    # Liste des tournois
    # --------------------------------------------------------------
    def list_tournaments(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        self.view.show_tournaments(tournaments)

    # --------------------------------------------------------------
    # Suppression d’un tournoi
    # --------------------------------------------------------------
    def delete_tournament(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]

        if not tournaments:
            console.print("[yellow]Aucun tournoi à supprimer.[/yellow]")
            return

        self.view.show_tournaments(tournaments)
        choice = console.input("Numéro du tournoi à supprimer : ")

        try:
            index = int(choice) - 1
            tournament = tournaments[index]
        except (ValueError, IndexError) as e:
            console.print(f"[red]Choix invalide : {e}[/red]")
            return

        confirm = console.input(
            f"Supprimer le tournoi '{tournament.name}' ? (o/N) : "
        ).lower()

        if confirm != "o":
            console.print("[yellow]Suppression annulée.[/yellow]")
            return

        tournaments_table.remove(TournamentQuery.name == tournament.name)
        console.print(f"[green]Tournoi '{tournament.name}' supprimé avec succès ![/green]")

    # --------------------------------------------------------------
    # Menu de gestion d’un tournoi
    # --------------------------------------------------------------
    def manage_tournament(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        tournament = self.view.select_tournament(tournaments)

        if not tournament:
            return

        all_players = PlayerController().get_all_players()
        tournament.players = [
            p for p in all_players if p.national_id in tournament.players_ids
        ]

        self.manage_selected_tournament(tournament)

    def manage_selected_tournament(self, tournament):
        while True:
            choice = self.view.manage_menu(tournament)

            if choice == "1":
                self.add_players_to_tournament(tournament)

            elif choice == "2":
                self.start_round(tournament)

            elif choice == "3":
                self.view.show_rounds(tournament)

            elif choice == "4":
                self.show_final_ranking(tournament)

            elif choice == "0":
                self._save_tournament(tournament)
                return

            else:
                console.print("[red]Choix invalide.[/red]")

    # --------------------------------------------------------------
    # Ajout des joueurs
    # --------------------------------------------------------------
    def add_players_to_tournament(self, tournament):
        players = PlayerController().get_all_players()
        selected = self.view.select_players(players)

        if not selected:
            return

        for p in selected:
            if p.national_id not in tournament.players_ids:
                tournament.players.append(p)
                tournament.players_ids.append(p.national_id)

        self._save_tournament(tournament)
        console.print("[green]Joueurs ajoutés au tournoi ![/green]")

    # --------------------------------------------------------------
    # Round Robin — génère des IDs
    # --------------------------------------------------------------
    def generate_round_robin_pairs(self, players):
        players = players[:]  # copie

        if len(players) % 2 == 1:
            players.append(None)

        n = len(players)
        rounds = []

        for _ in range(n - 1):
            round_pairs = []

            for i in range(n // 2):
                p1 = players[i]
                p2 = players[n - 1 - i]

                if p1 and p2:
                    round_pairs.append((p1.national_id, p2.national_id))

            players = [players[0]] + [players[-1]] + players[1:-1]
            rounds.append(round_pairs)

        return rounds

    # --------------------------------------------------------------
    # Lancer un round
    # --------------------------------------------------------------
    def start_round(self, tournament):

        if not tournament.generated_rounds:
            tournament.generated_rounds = self.generate_round_robin_pairs(
                tournament.players
            )
            tournament.current_round_index = 0

        if tournament.current_round_index >= len(tournament.generated_rounds):
            console.print("[yellow]Tous les rounds ont déjà été joués.[/yellow]")
            return

        pairs = tournament.generated_rounds[tournament.current_round_index]
        round_name = f"Round {tournament.current_round_index + 1}"
        new_round = Round(round_name)

        for pid1, pid2 in pairs:
            match = Match(pid1, pid2)
            new_round.matches.append(match)

        tournament.rounds.append(new_round)
        tournament.current_round_index += 1

        self._save_tournament(tournament)
        self.round_view.round_started(new_round)

        for match in new_round.matches:
            s1, s2 = self.round_view.ask_match_result(match)
            match.score1 = s1
            match.score2 = s2

        self._save_tournament(tournament)

        if tournament.current_round_index == len(tournament.generated_rounds):
            self.compute_final_ranking(tournament)

        console.print("[green]Round terminé ![/green]")

    # --------------------------------------------------------------
    # Calcul du classement final
    # --------------------------------------------------------------
    def compute_final_ranking(self, tournament):

        scores = {pid: 0 for pid in tournament.players_ids}

        for r in tournament.rounds:
            for m in r.matches:
                scores[m.player1] += m.score1
                scores[m.player2] += m.score2

        ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        tournament.final_ranking = ranking

        self._save_tournament(tournament)
        self.show_final_ranking(tournament)

    # --------------------------------------------------------------
    # Affichage du classement final
    # --------------------------------------------------------------
    def show_final_ranking(self, tournament):

        if not tournament.final_ranking:
            console.print("[yellow]Le classement final n'est pas encore disponible.[/yellow]")
            return

        all_players = PlayerController().get_all_players()
        lookup = {p.national_id: p for p in all_players}

        text = "[bold cyan]Classement final[/bold cyan]\n\n"

        for i, (pid, score) in enumerate(tournament.final_ranking, start=1):
            p = lookup.get(pid)
            if p:
                text += f"{i}. {p.first_name} {p.last_name} ({pid}) — {score} pts\n"

        console.print(Panel.fit(text))

    # --------------------------------------------------------------
    # Sauvegarde
    # --------------------------------------------------------------
    def _save_tournament(self, tournament):
        tournaments_table.update(
            tournament.to_dict(),
            TournamentQuery.name == tournament.name
        )
