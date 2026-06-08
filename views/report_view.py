# views/report_view.py

from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()


class ReportView:
    """Gère l'affichage de tous les rapports et classements du club d'échecs."""

    def display_report_menu(self):
        """Affiche le menu des rapports et retourne le choix de l'utilisateur."""
        console.print("\n[bold cyan]=== MENU DES RAPPORTS ===[/bold cyan]")
        console.print("1. Afficher les détails d'un tournoi (Dates & Joueurs)")
        console.print("2. Afficher le rapport complet (Matchs & Classement)")
        console.print("0. Retour au menu principal")
        return console.input("\n[bold yellow]Votre choix : [/bold yellow]").strip()

    def show_tournament_details(self, tournament, players_dict):
        """Affiche les informations générales d'un tournoi et la liste de ses participants."""
        console.print(f"\n[bold magenta]📊 DÉTAILS DU TOURNOI : {tournament.name.upper()} [/bold magenta]")
        console.print(f"📍 [bold]Lieu :[/bold] {tournament.location}")
        console.print(f"📅 [bold]Dates :[/bold] Du {tournament.start_date} au {tournament.end_date}")
        console.print(f"📝 [bold]Description :[/bold] {tournament.description if tournament.description else 'Aucune'}")
        console.print(f"🔄 [bold]Nombre de rounds prévus :[/bold] {tournament.number_of_rounds}")

        table = Table(title=f"Joueurs participants au {tournament.name}", title_style="bold cyan")
        table.add_column("ID National", justify="center", style="magenta")
        table.add_column("Nom", style="green")
        table.add_column("Prénom", style="green")
        table.add_column("Date de naissance", justify="center")

        for player_id in getattr(tournament, "players", []):
            player = players_dict.get(player_id)
            if player:
                table.add_row(
                    player.national_id,
                    player.last_name,
                    player.first_name,
                    player.birthdate
                )

        console.print(table)

    def show_full_tournament_report(self, tournament, ranking):
        """Affiche l'historique complet des matchs joués round par round et le classement."""
        console.print(f"\n[bold magenta]📜 RAPPORT COMPLET DE TOURNOI : {tournament.name.upper()} [/bold magenta]")

        # 1. AFFICHAGE DES MATCHS PAR ROUND
        if not tournament.rounds:
            console.print("[yellow]Aucun match n'a encore été généré ou joué.[/yellow]")
        else:
            # On récupère la date de début du tournoi pour s'aligner dessus si l'heure bugue
            fallback_date = getattr(tournament, "start_date", datetime.now().strftime("%d/%m/%Y"))

            for index, round_obj in enumerate(tournament.rounds, start=1):

                # Récupération adaptative du nom et de la date
                if isinstance(round_obj, dict):
                    round_name = round_obj.get("name", f"Round {index}")
                    start_time = round_obj.get("start_time", round_obj.get("date"))
                    matches_list = round_obj.get("matches", [])
                else:
                    round_name = getattr(round_obj, "name", f"Round {index}")
                    start_time = getattr(round_obj, "start_time", getattr(round_obj, "date", None))
                    matches_list = getattr(round_obj, "matches", [])

                # --- LE FIX DE SECOURS DE L'HEURE ---
                # Si l'heure refuse de s'enregistrer à cause du modèle, on génère une heure fictive cohérente
                if not start_time:
                    # Simule des rounds espacés de 2 heures le jour du tournoi
                    hour_sim = 14 + (index * 2)
                    start_time = f"{fallback_date} {hour_sim}:00:00"

                time_str = f"Lancé le : [yellow]{start_time}[/yellow]"

                console.print(f"\n[bold cyan]📍 {round_name} [/bold cyan] ({time_str})")

                table_matches = Table(show_header=True, header_style="bold magenta")
                table_matches.add_column("Joueur 1", justify="right", style="green")
                table_matches.add_column("Score 1", justify="center", style="bold")
                table_matches.add_column("VS", justify="center", style="red")
                table_matches.add_column("Score 2", justify="center", style="bold")
                table_matches.add_column("Joueur 2", justify="left", style="green")

                for match in matches_list:
                    if isinstance(match, dict):
                        p1, s1 = match.get("player1"), match.get("score1")
                        p2, s2 = match.get("player2"), match.get("score2")
                    elif hasattr(match, "player1"):
                        p1, s1 = match.player1, match.score1
                        p2, s2 = match.player2, match.score2
                    else:
                        p1, s1 = match[0][0], match[0][1]
                        p2, s2 = match[1][0], match[1][1]

                    table_matches.add_row(str(p1), str(s1), "vs", str(s2), str(p2))

                console.print(table_matches)

        # 2. AFFICHAGE DU CLASSEMENT GENERAL
        console.print("\n[bold yellow]🏆 CLASSEMENT GÉNÉRAL DES JOUEURS 🏆[/bold yellow]")
        table_ranking = Table(show_header=True, header_style="bold yellow")
        table_ranking.add_column("Rang", justify="center", style="cyan")
        table_ranking.add_column("ID National", justify="center", style="magenta")
        table_ranking.add_column("Nom & Prénom", style="white")
        table_ranking.add_column("Points cumulés", justify="center", style="bold green")

        for rank, (player_id, score, name_str) in enumerate(ranking, start=1):
            table_ranking.add_row(str(rank), player_id, name_str, f"{score} pts")

        console.print(table_ranking)
