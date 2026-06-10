from rich.console import Console
from rich.table import Table

console = Console()


class ReportView:
    """Affichage des rapports."""

    def display_report_menu(self):
        console.print("\n[bold green]=== RAPPORTS ===[/bold green]")
        console.print("1. Liste des tournois")
        console.print("2. Détails d’un tournoi")
        console.print("3. Historique complet")
        console.print("0. Retour")
        return console.input("\n[bold yellow]Votre choix : [/bold yellow]").strip()

    # ----------------------------------------------------------------------
    # DÉTAIL D’UN TOURNOI
    # ----------------------------------------------------------------------
    def show_tournament_details(self, tournament, players_dict):
        console.print(f"\n[bold gold1]DÉTAILS DU TOURNOI : {tournament.name}[/bold gold1]\n")

        console.print(f"Lieu : [white]{tournament.location}[/white]")
        console.print(f"Dates : [bold bright_blue]{tournament.start_date} → {tournament.end_date}[/bold bright_blue]")
        console.print(f"Description : [white]{tournament.description or 'Aucune'}[/white]")
        console.print(f"Rounds prévus : [bold yellow]{tournament.number_of_rounds}[/bold yellow]")

        table = Table(show_header=True, header_style="bold green", border_style="dim")
        table.add_column("ID", justify="center")
        table.add_column("Nom")
        table.add_column("Prénom")
        table.add_column("Naissance", justify="center")

        for p_id in tournament.players:
            p = players_dict.get(p_id)
            if p:
                table.add_row(p.national_id, p.last_name, p.first_name, p.birthdate)
            else:
                table.add_row(p_id, "Inconnu", "Inconnu", "N/A")

        console.print(table)

    # ----------------------------------------------------------------------
    # RAPPORT COMPLET (Rounds + Matchs + Classement)
    # ----------------------------------------------------------------------
    def show_full_tournament_report(self, tournament, ranking, players_data):
        console.print(f"\n[bold gold1]RAPPORT COMPLET : {tournament.name}[/bold gold1]\n")

        # -------------------------
        # AFFICHAGE DES ROUNDS
        # -------------------------
        for i, r in enumerate(tournament.rounds, 1):
            console.print(f"[bold]Round {i}[/bold] — {r.start_time}")

            table = Table(show_header=True, header_style="bold green", border_style="dim")
            table.add_column("Joueur 1")
            table.add_column("S1", justify="center")
            table.add_column("S2", justify="center")
            table.add_column("Joueur 2")

            for m in r.matches:

                # Extraction robuste : dict / objet Match / tuple
                if isinstance(m, dict):
                    p1_id = m.get("player1")
                    p2_id = m.get("player2")
                    s1 = m.get("score1", 0)
                    s2 = m.get("score2", 0)

                elif hasattr(m, "player1"):
                    p1_id = m.player1
                    p2_id = m.player2
                    s1 = m.score1
                    s2 = m.score2

                else:  # ancien format tuple/liste
                    p1_id, s1 = m[0]
                    p2_id, s2 = m[1]

                # Conversion ID → nom complet si disponible
                p1 = players_data.get(p1_id, p1_id)
                p2 = players_data.get(p2_id, p2_id)

                table.add_row(p1, str(s1), str(s2), p2)

            console.print(table)

        # -------------------------
        # CLASSEMENT FINAL
        # -------------------------
        console.print("\n[bold gold1]CLASSEMENT FINAL[/bold gold1]\n")

        table = Table(show_header=True, header_style="bold green", border_style="dim")
        table.add_column("Rang", justify="center")
        table.add_column("ID", justify="center")
        table.add_column("Nom")
        table.add_column("Points", justify="center")

        for rank, (p_id, score, name) in enumerate(ranking, 1):
            table.add_row(str(rank), p_id, name, f"{score:.1f}")

        console.print(table)
