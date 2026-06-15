from rich.console import Console
from rich.table import Table

console = Console()


class ReportView:
    """Affichage des rapports."""

    # ---------------------------------------------------------
    # LISTE DES TOURNOIS
    # ---------------------------------------------------------
    def show_tournament_list(self, tournaments):
        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("N°", justify="center")
        table.add_column("Nom")
        table.add_column("Lieu")
        table.add_column("Dates")

        for i, t in enumerate(tournaments, 1):
            table.add_row(
                str(i),
                t.name,
                t.location,
                f"{t.start_date} → {t.end_date}"
            )

        console.print(table)

    # ---------------------------------------------------------
    # DÉTAIL D’UN TOURNOI
    # ---------------------------------------------------------
    def show_tournament_details(self, tournament, players_dict):
        console.print(f"\n[bold gold1]DÉTAILS DU TOURNOI : {tournament.name}[/bold gold1]\n")

        console.print(f"Lieu : {tournament.location}")
        console.print(f"Dates : {tournament.start_date} → {tournament.end_date}")
        console.print(f"Description : {tournament.description or 'Aucune'}")
        console.print(f"Rounds prévus : {tournament.number_of_rounds}")

        table = Table(show_header=True, header_style="bold green")
        table.add_column("ID")
        table.add_column("Nom")
        table.add_column("Prénom")
        table.add_column("Naissance")

        for pid in tournament.players:
            p = players_dict.get(pid)
            if p:
                table.add_row(p.national_id, p.last_name, p.first_name, p.birthdate)
            else:
                table.add_row(pid, "Inconnu", "Inconnu", "N/A")

        console.print(table)

    # ---------------------------------------------------------
    # RAPPORT COMPLET
    # ---------------------------------------------------------
    def show_full_tournament_report(self, tournament, ranking, players_data):
        console.print(f"\n[bold gold1]RAPPORT COMPLET : {tournament.name}[/bold gold1]\n")

        for i, r in enumerate(tournament.rounds, 1):
            console.print(f"[bold]Round {i}[/bold] — {r.start_time}")

            table = Table(show_header=True, header_style="bold green")
            table.add_column("Joueur 1")
            table.add_column("S1")
            table.add_column("S2")
            table.add_column("Joueur 2")

            for m in r.matches:
                if isinstance(m, dict):
                    p1, s1 = m["player1"], m["score1"]
                    p2, s2 = m["player2"], m["score2"]
                else:
                    p1, s1 = m.player1, m.score1
                    p2, s2 = m.player2, m.score2

                table.add_row(
                    players_data.get(p1, p1),
                    str(s1),
                    str(s2),
                    players_data.get(p2, p2)
                )

            console.print(table)

        console.print("\n[bold gold1]CLASSEMENT FINAL[/bold gold1]\n")

        table = Table(show_header=True, header_style="bold green")
        table.add_column("Rang")
        table.add_column("ID")
        table.add_column("Nom")
        table.add_column("Points")

        for rank, (pid, score, name) in enumerate(ranking, 1):
            table.add_row(str(rank), pid, name, f"{score:.1f}")

        console.print(table)
