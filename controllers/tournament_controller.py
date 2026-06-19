# controllers/tournament_controller.py

from datetime import datetime
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from models.player import Player
from database import tournaments_table, players_table, TournamentQuery
from views.tournament_view import TournamentView
from controllers.round_controller import RoundController
from rich.console import Console

console = Console()


class TournamentController:
    """Logique métier des tournois : création, rounds, blocages."""

    def __init__(self):
        self.view = TournamentView()
        self.round_controller = RoundController()

    def create_tournament(self):
        """Création d'un tournoi."""
        # 1. On affiche la liste des tournois existants pour aider l'utilisateur
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        self.view.show_tournaments(tournaments)

        data = self.view.ask_tournament_info()
        if not data:
            return

        tournament = Tournament(**data)
        tournaments_table.insert(tournament.to_dict())
        console.print("[green]Tournoi créé avec succès ![/green]")

    def list_tournaments(self):
        """Liste des tournois."""
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        self.view.show_tournaments(tournaments)

    def manage_tournament(self):
        """Pilotage et gestion des étapes d'un tournoi."""
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        if not tournaments:
            console.print("[yellow]Aucun tournoi disponible.[/yellow]")
            return

        self.view.show_tournaments(tournaments)
        choice = console.input("\nNuméro du tournoi à piloter : ").strip()

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(tournaments):
            console.print("[red]Numéro invalide.[/red]")
            return

        tournament = tournaments[int(choice) - 1]

        while True:
            # On recharge les données depuis la base pour être à jour
            raw_t = tournaments_table.get(TournamentQuery.name == tournament.name)
            if not raw_t:
                break
            tournament = Tournament.from_dict(raw_t)

            manage_choice = self.view.display_manage_menu(tournament).strip()

            if manage_choice == "1":
                self.add_players_to_tournament(tournament)
            elif manage_choice == "2":
                self.generate_next_round(tournament)
            elif manage_choice == "3":
                self.play_round_scores(tournament)
            elif manage_choice == "0":
                break
            else:
                console.print("[red]Choix invalide.[/red]")

    def add_players_to_tournament(self, tournament):
        """Sélectionne et ajoute exactement 4 joueurs actifs au tournoi."""
        if len(tournament.players) == 4:
            console.print("[yellow]Ce tournoi compte déjà ses 4 participants.[/yellow]")
            return

        # Récupération de tous les joueurs et conversion en objets Player
        all_players = [Player.from_dict(p) for p in players_table.all()]

        # On ne garde que les joueurs actifs
        active_players = [p for p in all_players if getattr(p, "is_active", True)]

        if len(active_players) < 4:
            console.print("[red]Erreur : Il faut au moins 4 joueurs actifs enregistrés en base.[/red]")
            return

        selected_ids = self.view.select_4_players(active_players)

        tournament.players = selected_ids
        tournaments_table.update(
            {"players": tournament.players},
            TournamentQuery.name == tournament.name
        )
        console.print("[green]Les 4 joueurs ont été inscrits avec succès ![/green]")

    def generate_next_round(self, tournament):
        """Génère le prochain Round selon l'algorithme de Berger (pas de doublon)."""
        # 1. Vérifications initiales
        if len(tournament.players) < 4:
            console.print("[red]Erreur : Il faut exactement 4 joueurs sélectionnés pour générer les rounds.[/red]")
            return

        if len(tournament.rounds) >= tournament.number_of_rounds:
            console.print("[yellow]Le tournoi est déjà terminé (3 rounds joués).[/yellow]")
            return

        # Vérification si le round précédent est bien clôturé (scores saisis)
        if tournament.rounds:
            last_round = tournament.rounds[-1]
            matches = last_round.get("matches", []) if isinstance(last_round, dict) else last_round.matches
            for m in matches:
                s1 = m.get("score1") if isinstance(m, dict) else m.score1
                s2 = m.get("score2") if isinstance(m, dict) else m.score2
                if s1 == 0.0 and s2 == 0.0:
                    console.print("[red]Erreur : Saisir les scores du round avant de générer le round suivant.[/red]")
                    return

        # 2. ALGORITHME DE BERGER (Strict et fixe pour 4 joueurs)
        p = tournament.players  # Liste stable contenant les 4 IDs [ID1, ID2, ID3, ID4]
        current_round_number = len(tournament.rounds) + 1
        round_matches = []

        if current_round_number == 1:
            # Round 1 : 1 vs 4 et 2 vs 3
            round_matches.append(Match(player1=p[0], player2=p[3]))
            round_matches.append(Match(player1=p[1], player2=p[2]))

        elif current_round_number == 2:
            # Round 2 : 1 vs 3 et 4 vs 2
            round_matches.append(Match(player1=p[0], player2=p[2]))
            round_matches.append(Match(player1=p[3], player2=p[1]))

        elif current_round_number == 3:
            # Round 3 : 1 vs 2 et 3 vs 4
            round_matches.append(Match(player1=p[0], player2=p[1]))
            round_matches.append(Match(player1=p[2], player2=p[3]))

        # 3. Création et sauvegarde du Round
        current_now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        new_round_obj = Round(
            name=f"Round {current_round_number}",
            matches=round_matches,
            start_time=current_now_str,
            end_time=""
        )

        tournament.rounds.append(new_round_obj)

        # Enregistrement sérialisé complet dans TinyDB
        tournaments_table.update(
            {"rounds": [r.to_dict() if hasattr(r, "to_dict") else r for r in tournament.rounds]},
            TournamentQuery.name == tournament.name
        )

        console.print(f"[green]Le {new_round_obj.name} a été généré avec succès ![/green]")

    def play_round_scores(self, tournament):
        """Appelle le contrôleur secondaire pour la saisie des scores."""
        if not tournament.rounds:
            console.print("[yellow]Aucun round n'a encore été généré pour ce tournoi.[/yellow]")
            return

        self.round_controller.enter_results(tournament)
        console.print("[green]Scores du round enregistrés ![/green]")

    def delete_tournament(self):
        """Supprime un tournoi de la base."""
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        self.view.show_tournaments(tournaments)
        choice = console.input("Numéro du tournoi à supprimer : ").strip()

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(tournaments):
            console.print("[red]Numéro invalide.[/red]")
            return

        tournament_to_del = tournaments[int(choice) - 1]
        tournaments_table.remove(TournamentQuery.name == tournament_to_del.name)
        console.print(f"[green]Le tournoi '{tournament_to_del.name}' a bien été supprimé.[/green]")
