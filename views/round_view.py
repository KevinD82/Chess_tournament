# views/round_view.py

from rich.console import Console
from rich.panel import Panel

console = Console()


class RoundView:
    """Gère l'affichage et les saisies liées aux rounds et aux matchs."""

    def ask_match_result(self, match):
        """Demande le résultat d'un match et applique un contrôle de saisie strict."""

        # Récupération propre des identifiants des joueurs
        p1 = match.player1 if hasattr(match, "player1") else match.get("player1", "Joueur 1")
        p2 = match.player2 if hasattr(match, "player2") else match.get("player2", "Joueur 2")

        match_text = (
            f"[bold white][1][/bold white] [green]{p1}[/green]\n"
            f"[bold white][2][/bold white] [green]{p2}[/green]\n\n"
            f"[bold yellow]Options :[/bold yellow] "
            f"[cyan][1][/cyan] Victoire {p1} | [cyan][2][/cyan] Victoire {p2} | [cyan][N][/cyan] Match Nul"
        )

        console.print(Panel(match_text, title="Résultat du match", border_style="blue"))

        while True:
            choice = console.input("[bold yellow]Votre choix (1, 2 ou N) : [/bold yellow]").strip().upper()

            if choice in ["1", "2", "N"]:
                return choice

            console.print("[red]❌ Saisie invalide ! Vous devez obligatoirement entrer 1, 2 ou N.[/red]")
