# controllers/menu_controller.py

# Importation des différents contrôleurs utilisés par le menu principal.
# Chaque contrôleur gère une partie spécifique de l'application :
# - PlayerController : création et gestion des joueurs
# - TournamentController : création et gestion des tournois
# - ReportController : génération des rapports et historique
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController

# Importation de la vue du menu, qui affiche les options à l'utilisateur.
from views.menu_view import MenuView


class MenuController:
    """
    Le MenuController est le point d'entrée principal de l'application.
    Il orchestre la navigation entre les différentes fonctionnalités.
    """

    def __init__(self):
        # Instanciation des contrôleurs secondaires
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.report_controller = ReportController()

        # Vue du menu principal
        self.view = MenuView()

    def run(self):
        """
        Boucle principale de l'application.
        Affiche le menu, récupère le choix utilisateur,
        et redirige vers la fonctionnalité correspondante.
        """
        while True:
            # Affiche le menu principal et récupère le choix
            choice = self.view.main_menu()

            # Si l'utilisateur tape "echap" ou "annuler", safe_input renvoie None
            if choice is None:
                continue  # On réaffiche simplement le menu

            # 1. Création d'un joueur
            if choice == "1":
                self.player_controller.create_player()

            # 2. Affichage de la liste des joueurs
            elif choice == "2":
                self.player_controller.list_players()

            # 3. Création d'un tournoi
            elif choice == "3":
                self.tournament_controller.create_tournament()

            # 4. Liste des tournois existants
            elif choice == "4":
                self.tournament_controller.list_tournaments()

            # 5. Gestion d'un tournoi (rounds, résultats…)
            elif choice == "5":
                self.tournament_controller.manage_tournament()

            # 6. Accès au sous-menu des rapports
            elif choice == "6":
                self.report_menu()

            # 0. Quitter l'application
            elif choice == "0":
                self.view.exit_message()
                break

    def report_menu(self):
        """
        Sous-menu dédié aux rapports :
        - liste des joueurs
        - liste des tournois
        - détails d’un tournoi
        - rounds
        - matchs
        - scores finaux
        - historique complet
        """
        while True:
            choice = self.view.report_menu()

            # Annulation → retour au menu principal
            if choice is None:
                return

            # 1. Liste de tous les joueurs
            if choice == "1":
                self.report_controller.list_all_players()

            # 2. Liste de tous les tournois
            elif choice == "2":
                self.report_controller.list_all_tournaments()

            # 3. Détails d’un tournoi
            elif choice == "3":
                self.report_controller.tournament_details()

            # 4. Rounds d’un tournoi
            elif choice == "4":
                self.report_controller.tournament_rounds()

            # 5. Matchs d’un tournoi
            elif choice == "5":
                self.report_controller.tournament_matches()

            # 6. Scores finaux
            elif choice == "6":
                self.report_controller.tournament_scores()

            # 7. Historique complet
            elif choice == "7":
                self.report_controller.full_history()

            # 0. Retour au menu principal
            elif choice == "0":
                return
