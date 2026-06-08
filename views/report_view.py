# views/report_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class ReportView:
    """Gère l'affichage visuel de tous les rapports et classements du système."""

    def display_report_menu(self):
        """Affiche le sous-menu des rapports et retourne le choix sélectionné."""
        console.print("\n[bold magenta]=== MENU DES RAPPORTS ===[/bold magenta]")
        console.print("1. Détails du tournoi (Lieu, Dates, Liste des joueurs)")
        console.print("2. Rapport complet (Liste des rounds, Matchs joués, Classement final)")
        console.print("0. Retour au menu principal")
        return console.input("\n[bold yellow]Votre choix : [/bold yellow]").strip()

    def show_tournament_details(self, tournament, players_dict):
        """Affiche les métadonnées structurelles d'un tournoi et sa liste de participants."""
        title_text = f"[bold]📊 DÉTAILS DU TOURNOI : {tournament.name.upper()}[/bold]"
        console.print(Panel(title_text, border_style="magenta"))

        console.print(f"📍 [bold cyan]Lieu :[/bold cyan] {tournament.location}")
        console.print(f"📅 [bold cyan]Dates :[/bold cyan] Du {tournament.start_date} au {tournament.end_date}")
        console.print(
            f"📝 [bold cyan]Description :[/bold cyan] {tournament.description if tournament.description else 'Aucune'}"
        )

        total_rounds = getattr(
            tournament, "number_of_rounds", getattr(
                tournament, "num_rounds", getattr(
                    tournament, "total_rounds", 4
                )
            )
        )
        console.print(f"🔄 [bold cyan]Nombre de rounds prévus :[/bold cyan] {total_rounds}")

        console.print("\n[bold cyan]⚡ Joueurs participants au Tournoi[/bold cyan]")
        # Remplacement de "gray" par "dim" pour éviter l'erreur de style Rich
        table = Table(border_style="dim")
        table.add_column("ID National", style="magenta", justify="center")
        table.add_column("Nom", style="green")
        table.add_column("Prénom", style="green")
        table.add_column("Date de naissance", justify="center")

        for p_id in tournament.players:
            player_obj = players_dict.get(p_id)
            if player_obj:
                # Récupération adaptative sécurisée de la date de naissance
                b_date = getattr(player_obj, "birthdate", getattr(player_obj, "birth_date", "N/A"))

                table.add_row(
                    player_obj.national_id,
                    player_obj.last_name,
                    player_obj.first_name,
                    b_date
                )
            else:
                table.add_row(p_id, "Inconnu", "Inconnu", "N/A")

        console.print(table)

    def show_full_tournament_report(self, tournament, ranking, players_data=None):
        """Affiche l'historique complet des rounds avec les noms réels et le classement final."""
        if players_data is None:
            players_data = {}

        report_title = f"[bold]📜 RAPPORT COMPLET DE TOURNOI : {tournament.name.upper()}[/bold]"
        console.print(Panel(report_title, border_style="magenta"))

        # 1. PARCOURS ET AFFICHAGE SYNCHRONISÉ DES MATCHS DE CHAQUE ROUND
        for index, round_obj in enumerate(tournament.rounds, start=1):
            if isinstance(round_obj, dict):
                r_name = round_obj.get("name", f"Round {index}")
                r_time = round_obj.get("start_time", round_obj.get("date", "Non spécifiée"))
                matches = round_obj.get("matches", [])
            else:
                r_name = getattr(round_obj, "name", f"Round {index}")
                r_time = getattr(round_obj, "start_time", getattr(round_obj, "date", "Non spécifiée"))
                matches = getattr(round_obj, "matches", [])

            time_display = (
                f"Lancé le : {r_time}" if "non" not in r_time.lower() and r_time
                else "Date de lancement non spécifiée"
            )
            console.print(f"\n📍 [bold cyan]{r_name}[/bold cyan]  ({time_display})")

            # Remplacement de "gray" par "dim" ici aussi
            table = Table(border_style="dim")
            table.add_column("Joueur 1", style="green", justify="left", min_width=25)
            table.add_column("Score 1", justify="center", style="bold white")
            table.add_column("VS", justify="center", style="magenta")
            table.add_column("Score 2", justify="center", style="bold white")
            table.add_column("Joueur 2", style="green", justify="left", min_width=25)

            for match in matches:
                if isinstance(match, dict):
                    p1_id, s1 = match.get("player1"), match.get("score1", 0.0)
                    p2_id, s2 = match.get("player2"), match.get("score2", 0.0)
                elif hasattr(match, "player1"):
                    p1_id, s1 = match.player1, getattr(match, "score1", 0.0)
                    p2_id, s2 = match.player2, getattr(match, "score2", 0.0)
                else:
                    p1_id, s1 = match[0][0], match[0][1]
                    p2_id, s2 = match[1][0], match[1][1]

                # Conversion ID -> "NOM Prénom (ID)" pour le tableau des matchs
                p1_name = players_data.get(p1_id, "Joueur Inconnu")
                p2_name = players_data.get(p2_id, "Joueur Inconnu")

                p1_display = f"{p1_name} ({p1_id})" if p1_name != "Joueur Inconnu" else p1_id
                p2_display = f"{p2_name} ({p2_id})" if p2_name != "Joueur Inconnu" else p2_id

                table.add_row(p1_display, f"{float(s1):.1f}", "vs", f"{float(s2):.1f}", p2_display)

            console.print(table)

        # 2. AFFICHAGE DU CLASSEMENT GÉNÉRAL FINAL
        console.print("\n\n🏆 [bold yellow]CLASSEMENT GÉNÉRAL DES JOUEURS[/bold yellow] 🏆")
        rank_table = Table(border_style="gold1")
        rank_table.add_column("Rang", justify="center", style="cyan")
        rank_table.add_column("ID National", justify="center", style="magenta")
        rank_table.add_column("Nom & Prénom", style="white")
        rank_table.add_column("Points cumulés", justify="center", style="green bold")

        for rank, (p_id, score, name) in enumerate(ranking, start=1):
            rank_table.add_row(str(rank), p_id, name, f"{score:.1f} pts")

        console.print(rank_table)
