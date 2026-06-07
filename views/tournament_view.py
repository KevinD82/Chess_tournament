# views/tournament_view.py

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class TournamentView:

    def ask_tournament_info(self):
        console.print(Panel.fit("[bold cyan]Création d'un tournoi[/bold cyan]"))

        name = console.input("Nom du tournoi : ")
        location = console.input("Lieu : ")
        start_date = console.input("Date de début (JJ/MM/AAAA) : ")
        end_date = console.input("Date de fin (JJ/MM/AAAA) : ")
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
        table.add_column("Début", style="magenta")
        table.add_column("Fin", style="magenta")

        for i, t in enumerate(tournaments, start=1):
            start = f"{t.start_date} {t.start_time}".strip()
            end = f"{t.end_date} {t.end_time}".strip()
            table.add_row(str(i), t.name, t.location, start, end)

        console.print(table)

    def show_round(self, round_number, matches):
        console.print(Panel.fit(f"[bold cyan]Round {round_number}[/bold cyan]"))
        for m in matches:
            console.print(f"{m['p1']} vs {m['p2']}")

    def ask_score(self, p1, p2):
        console.print(f"Score pour {p1} vs {p2} :")
        while True:
            try:
                s1 = float(console.input(f"Score de {p1} : ").replace(",", "."))
                s2 = float(console.input(f"Score de {p2} : ").replace(",", "."))
                return s1, s2
            except ValueError:
                console.print("[red]Veuillez entrer un nombre valide (0, 0.5 ou 1).[/red]")

    def show_results(self, results):
        console.print(Panel.fit("[bold green]Résultats du tournoi[/bold green]"))

        table = Table(title="Classement final")
        table.add_column("Position", style="yellow")
        table.add_column("Joueur", style="cyan")
        table.add_column("Score", style="magenta")

        for pos, (player, score) in enumerate(results, start=1):
            table.add_row(str(pos), player, str(score))

        console.print(table)
