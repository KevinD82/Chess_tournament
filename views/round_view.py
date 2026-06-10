from rich.console import Console
from rich.table import Table

console = Console()


class RoundView:
    """Saisie des résultats de match."""

    def ask_match_result(self, match, players_dict=None):
        # Récupération des noms complets si disponibles
        p1 = (
            players_dict.get(match.player1).last_name + " " +
            players_dict.get(match.player1).first_name
            if players_dict and match.player1 in players_dict
            else match.player1
        )

        p2 = (
            players_dict.get(match.player2).last_name + " " +
            players_dict.get(match.player2).first_name
            if players_dict and match.player2 in players_dict
            else match.player2
        )

        console.print(f"\n[bold cyan]Match : {p1} vs {p2}[/bold cyan]")

        # --- Tableau des choix ---
        table = Table(show_header=True, header_style="bold cyan", border_style="dim")
        table.add_column("Choix", justify="center")
        table.add_column("Signification", justify="left")

        table.add_row("[bold bright_blue]1[/bold bright_blue]", f"Victoire {p1}")
        table.add_row("[bold green]2[/bold green]", f"Victoire {p2}")
        table.add_row("[bold yellow]N[/bold yellow]", "Match nul")

        console.print(table)

        # --- Saisie utilisateur ---
        while True:
            choice = console.input("[bold yellow]Votre choix : [/bold yellow]").strip().upper()

            if choice in ("1", "2", "N"):
                return choice

            console.print("[red]Choix invalide.[/red]")
