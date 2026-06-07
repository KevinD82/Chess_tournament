# views/tournament_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class TournamentView:

    def ask_tournament_info(self):
        console.print(Panel.fit("[bold cyan]Création d'un tournoi[/bold cyan]"))

        name = console.input("Nom du tournoi : ")
        location = console.input("Lieu : ")
        start_date = console.input("Date de début : ")
        end_date = console.input("Date de fin : ")
        description = console.input("Description : ")

        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
        }

    def show_tournaments(self, tournaments):
        table = Table(title="Liste des tournois")

        table.add_column("N°", style="yellow")
        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="cyan")
        table.add_column("Dates", style="magenta")

        for i, t in enumerate(tournaments, start=1):
            table.add_row(
                str(i),
                t.name,
                t.location,
                f"{t.start_date} → {t.end_date}"
            )

        console.print(table)

    def show_round(self, round_number, matches):
        console.print(f"\n[bold cyan]Round {round_number}[/bold cyan]")
        for m in matches:
            console.print(f"- {m['p1']} vs {m['p2']}")

    def ask_score(self, p1, p2):
        console.print(f"\n[bold yellow]{p1} vs {p2}[/bold yellow]")
        s1 = float(console.input(f"Score {p1} : "))
        s2 = float(console.input(f"Score {p2} : "))
        return s1, s2

    def show_results(self, results):
        console.print("\n[bold green]=== Classement final ===[/bold green]")
        table = Table()

        table.add_column("Position")
        table.add_column("Joueur")
        table.add_column("Points")

        for i, (player, score) in enumerate(results, start=1):
            table.add_row(str(i), player, str(score))

        console.print(table)
