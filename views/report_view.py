# views/report_view.py

from rich.console import Console
from rich.table import Table

console = Console()


class ReportView:
    """Affichage des rapports et détails des tournois."""

    def display_report_menu(self):
        """Affiche le menu des rapports avec le choix du classement général."""
        console.print("\n[bold green]=== RAPPORTS ===[/bold green]")
        console.print("1. Liste des tournois")
        console.print("2. Détails d’un tournoi")
        console.print("3. Historique complet")
        console.print("4. Classement général (Tous tournois)")
        console.print("0. Retour")
        return console.input("\n[bold yellow]Votre choix : [/bold yellow]").strip()

    # ----------------------------------------------------------------------
    # DÉTAIL D’UN TOURNOI (Dynamique avec dates + heures réelles)
    # ----------------------------------------------------------------------
    def show_tournament_details(self, tournament, players_dict):
        console.print(f"\n[bold gold1]DÉTAILS DU TOURNOI : {tournament.name.upper()}[/bold gold1]\n")

        console.print(f"Lieu : [white]{tournament.location}[/white]")
        console.print(f"Description : [white]{tournament.description or 'Aucune'}[/white]")

        played_rounds_count = 0
        for r in tournament.rounds:
            if isinstance(r, dict):
                if r.get("end_time"):
                    played_rounds_count += 1
            else:
                if getattr(r, "end_time", None):
                    played_rounds_count += 1

        console.print(
            f"Nombre de rounds joués : [bold cyan]{played_rounds_count} / "
            f"{tournament.number_of_rounds}[/bold cyan]"
        )

        start_datetime = "Non commencé"
        end_datetime = "En cours"

        if tournament.rounds:
            first_round = tournament.rounds[0]
            if isinstance(first_round, dict):
                start_datetime = first_round.get("start_time", "Non spécifié")
            else:
                start_datetime = getattr(first_round, "start_time", "Non spécifié")

            if played_rounds_count == tournament.number_of_rounds:
                last_round = tournament.rounds[-1]
                if isinstance(last_round, dict):
                    end_datetime = last_round.get("end_time", "En cours")
                else:
                    end_datetime = getattr(last_round, "end_time", "En cours")

        console.print(f"Début réel : [bold bright_blue]{start_datetime}[/bold bright_blue]")
        console.print(f"Fin réelle  : [bold bright_blue]{end_datetime}[/bold bright_blue]\n")

        table = Table(show_header=True, header_style="bold green", border_style="dim")
        table.add_column("Joueurs Participants", justify="left")
        table.add_column("Statut", justify="center")

        for p_id in tournament.players:
            p = players_dict.get(p_id)
            if p:
                status = "[green]Actif[/green]" if getattr(p, "is_active", True) else "[red]Inactif[/red]"
                table.add_row(f"{p.last_name.upper()} {p.first_name} ({p_id})", status)
            else:
                table.add_row(f"Joueur inconnu ({p_id})", "[dim]N/A[/dim]")

        console.print(table)

    # ----------------------------------------------------------------------
    # HISTORIQUE / RAPPORT COMPLET D'UN TOURNOI
    # ----------------------------------------------------------------------
    def show_full_tournament_report(self, tournament, ranking, players_data):
        console.print("\n[bold magenta]==================================================[/bold magenta]")
        console.print(f"[bold cyan]RAPPORT COMPLET : {tournament.name.upper()}[/bold cyan]")
        console.print("[bold magenta]==================================================[/bold magenta]\n")

        console.print(f"Lieu : {tournament.location}")
        console.print(f"Description : {tournament.description or 'Aucune'}\n")

        console.print("[bold gold1]DÉROULEMENT DES MATCHS[/bold gold1]\n")

        for i, r in enumerate(tournament.rounds, 1):
            if isinstance(r, dict):
                r_name = r.get("name", f"Round {i}")
                r_start = r.get("start_time", "Inconnu")
                r_end = r.get("end_time", "En cours")
                matches = r.get("matches", [])
            else:
                r_name = getattr(r, "name", f"Round {i}")
                r_start = getattr(r, "start_time", "Inconnu")
                r_end = getattr(r, "end_time", "En cours")
                matches = getattr(r, "matches", [])

            console.print(
                f"[bold bright_blue]{r_name}[/bold bright_blue] — Début : {r_start} | "
                f"Fin : {r_end or 'En cours'}"
            )

            table = Table(show_header=True, header_style="bold cyan", border_style="dim")
            table.add_column("Joueur 1", justify="right", style="white")
            table.add_column("Score 1", justify="center", style="bold yellow")
            table.add_column("Score 2", justify="center", style="bold yellow")
            table.add_column("Joueur 2", justify="left", style="white")

            for m in matches:
                if isinstance(m, dict):
                    p1_id = m.get("player1")
                    p2_id = m.get("player2")
                    s1 = m.get("score1", 0.0)
                    s2 = m.get("score2", 0.0)
                else:
                    p1_id = getattr(m, "player1", "Inconnu")
                    p2_id = getattr(m, "player2", "Inconnu")
                    s1 = getattr(m, "score1", 0.0)
                    s2 = getattr(m, "score2", 0.0)

                p1_name = players_data.get(p1_id, p1_id)
                p2_name = players_data.get(p2_id, p2_id)

                table.add_row(p1_name, str(s1), str(s2), p2_name)

            console.print(table)
            console.print()

        console.print("[bold gold1]CLASSEMENT DU TOURNOI[/bold gold1]\n")

        table = Table(show_header=True, header_style="bold green", border_style="dim")
        table.add_column("Rang", justify="center")
        table.add_column("Nom Complet")
        table.add_column("Identifiant", justify="center")
        table.add_column("Score Total", justify="center", style="bold yellow")

        for rank, item in enumerate(ranking, 1):
            if isinstance(item, (tuple, list)) and len(item) >= 2:
                p_id = item[0]
                total_score = item[1]
            else:
                p_id = item
                total_score = "N/A"

            p_name = players_data.get(p_id, "Joueur Inconnu")
            table.add_row(str(rank), p_name, str(p_id), f"{total_score} pts")

        console.print(table)
        console.print("\n[dim]Fin du rapport.[/dim]")

    # ----------------------------------------------------------------------
    # CLASSEMENT GÉNÉRAL (Tous tournois confondus)
    # ----------------------------------------------------------------------
    def show_global_ranking(self, global_ranking, players_data):
        """Affiche le tableau du classement cumulé historique."""
        console.print("\n[bold gold1]=== CLASSEMENT GÉNÉRAL (TOUT TOURNOI CONFONDU) ===[/bold gold1]\n")

        if not global_ranking:
            console.print("[yellow]Aucun point n'a encore été marqué dans l'historique.[/yellow]")
            return

        table = Table(show_header=True, header_style="bold cyan", border_style="dim")
        table.add_column("Rang", justify="center", width=6)
        table.add_column("Nom Complet", width=35)
        table.add_column("ID National", justify="center", width=15)
        table.add_column("Score Cumulé", justify="center", style="bold yellow", width=15)

        for rank, (p_id, total_score) in enumerate(global_ranking, 1):
            p_name = players_data.get(p_id, "Joueur Inconnu")
            table.add_row(str(rank), p_name, str(p_id), f"{total_score} pts")

        console.print(table)
        console.print("\n[dim]Le classement est calculé sur la somme totale des scores enregistrés.[/dim]")
