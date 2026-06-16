# controllers/report_controller.py

from database import tournaments_table, players_table
from models.tournament import Tournament
from views.report_view import ReportView


class ReportController:
    """Contrôleur gérant la logique des rapports et classements."""

    def __init__(self):
        self.report_view = ReportView()

<<<<<<< HEAD
    def run(self):
        """Boucle principale du menu des rapports."""
        while True:
            choice = self.report_view.display_report_menu()

            if choice == "1":
                self.list_all_tournaments()
            elif choice == "2":
                self.show_specific_tournament_details()
            elif choice == "3":
                self.show_full_tournament_history()
            elif choice == "4":
                self.global_ranking_logic()
            elif choice == "0":
                break
            else:
                from rich.console import Console
                Console().print("[red]⚠ Choix invalide. Veuillez entrer un nombre entre 0 et 4.[/red]")

    def _select_tournament(self):
        """Méthode utilitaire interne pour sélectionner un tournoi dans la base."""
        from views.tournament_view import TournamentView
        tournaments_data = tournaments_table.all()
        
        if not tournaments_data:
            from rich.console import Console
            Console().print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return None

        # On affiche la liste pour que l'utilisateur puisse choisir
        t_view = TournamentView()
        tournaments_objects = [Tournament.from_dict(t) for t in tournaments_data]
        t_view.show_tournaments(tournaments_objects)

        choice = t_view.console.input("\n[bold yellow]Sélectionnez le numéro du tournoi : [/bold yellow]").strip()
        if not choice.isdigit():
            return None

        idx = int(choice) - 1
        if 0 <= idx < len(tournaments_objects):
            return tournaments_objects[idx]
        return None

    def list_all_tournaments(self):
        """Option 1 : Affiche la liste simplifiée de tous les tournois."""
        from views.tournament_view import TournamentView
        tournaments_data = tournaments_table.all()
        tournaments_objects = [Tournament.from_dict(t) for t in tournaments_data]
        TournamentView().show_tournaments(tournaments_objects)

    def show_specific_tournament_details(self):
        """Option 2 : Charge le tournoi sélectionné et affiche ses détails réels."""
        tournament = self._select_tournament()
        if tournament:
            # On charge les joueurs pour que la vue affiche les noms/statuts
            players_dict = {}
            from models.player import Player
            for p_data in players_table.all():
                players_dict[p_data["national_id"]] = Player.from_dict(p_data)
                
            self.report_view.show_tournament_details(tournament, players_dict)

    def show_full_tournament_history(self):
        """Option 3 : Affiche les rounds, matchs et le classement final du tournoi."""
        tournament = self._select_tournament()
        if tournament:
            # 1. Charger un dictionnaire d'ID -> "NOM Prénom"
            players_data = {}
            for p in players_table.all():
                players_data[p["national_id"]] = f"{p['last_name'].upper()} {p['first_name']}"

            # 2. Récupérer ou générer le classement du tournoi actuel
            # Si votre modèle Tournament possède une méthode de classement, utilisez-la,
            # sinon on extrait un classement de secours basé sur les joueurs enregistrés
            ranking = tournament.get_ranking() if hasattr(tournament, 'get_ranking') else tournament.players

            self.report_view.show_full_tournament_report(tournament, ranking, players_data)

    # ----------------------------------------------------------------------
    # Option 4 : CLASSEMENT GÉNÉRAL (Calculé sur tout l'historique)
    # ----------------------------------------------------------------------
    def global_ranking_logic(self):
        """Calcule et affiche le classement global toutes compétitions confondues."""
        players_data = {}
        for p in players_table.all():
            players_data[p["national_id"]] = f"{p['last_name'].upper()} {p['first_name']}"

        scores_globaux = {}
        
        for t_data in tournaments_table.all():
            rounds = t_data.get("rounds", [])
            for r in rounds:
                matches = r.get("matches", [])
                for m in matches:
                    p1 = m.get("player1")
                    p2 = m.get("player2")
                    s1 = m.get("score1")
                    s2 = m.get("score2")

                    if s1 is not None and s2 is not None:
                        scores_globaux[p1] = scores_globaux.get(p1, 0.0) + float(s1)
                        scores_globaux[p2] = scores_globaux.get(p2, 0.0) + float(s2)

        sorted_ranking = sorted(scores_globaux.items(), key=lambda item: item[1], reverse=True)
        self.report_view.show_global_ranking(sorted_ranking, players_data)
=======
    # ---------------------------------------------------------
    # LISTE DES TOURNOIS
    # ---------------------------------------------------------
    def report_tournaments(self):
        tournaments = [Tournament.from_dict(t) for t in tournaments_table.all()]
        self.view.show_tournament_list(tournaments)

    # ---------------------------------------------------------
    # DÉTAIL D’UN TOURNOI
    # ---------------------------------------------------------
    def report_tournament_details(self):
        raw_tournaments = tournaments_table.all()
        if not raw_tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        for i, t in enumerate(raw_tournaments, 1):
            console.print(f"{i}. {t['name']} ({t['location']})")

        choice = console.input("\nNuméro du tournoi : ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(raw_tournaments):
            console.print("[red]Numéro invalide.[/red]")
            return

        raw = raw_tournaments[int(choice) - 1]
        tournament = Tournament.from_dict(raw)

        players_dict = {p['national_id']: Player.from_dict(p) for p in players_table.all()}

        self.view.show_tournament_details(tournament, players_dict)

    # ---------------------------------------------------------
    # HISTORIQUE COMPLET
    # ---------------------------------------------------------
    def report_full_history(self):
        raw_tournaments = tournaments_table.all()
        if not raw_tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        for i, t in enumerate(raw_tournaments, 1):
            console.print(f"{i}. {t['name']} ({t['location']})")

        choice = console.input("\nNuméro du tournoi : ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(raw_tournaments):
            console.print("[red]Numéro invalide.[/red]")
            return

        raw = raw_tournaments[int(choice) - 1]
        tournament = Tournament.from_dict(raw)

        players_data = {
            p['national_id']: f"{p['last_name']} {p['first_name']}"
            for p in players_table.all()
        }

        # Calcul des scores
        scores = {pid: 0.0 for pid in tournament.players}

        for r in tournament.rounds:
            matches = r.matches if hasattr(r, "matches") else r.get("matches", [])
            for m in matches:
                if isinstance(m, dict):
                    p1, s1 = m["player1"], m["score1"]
                    p2, s2 = m["player2"], m["score2"]
                else:
                    p1, s1 = m.player1, m.score1
                    p2, s2 = m.player2, m.score2

                scores[p1] += float(s1)
                scores[p2] += float(s2)

        ranking = sorted(
            [(pid, score, players_data.get(pid, "Inconnu")) for pid, score in scores.items()],
            key=lambda x: x[1],
            reverse=True
        )

        self.view.show_full_tournament_report(tournament, ranking, players_data)
>>>>>>> 1511e2a3c98dd82fcb10c2c42a980ae48edac3ad
