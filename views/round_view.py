# views/round_view.py

from rich.console import Console
from rich.panel import Panel

console = Console()


class RoundView:

    # --------------------------------------------------------------
    # Affichage du début d’un round
    # --------------------------------------------------------------
    def round_started(self, round_obj):
        console.print(
            Panel.fit(
                f"[bold cyan]=== Début du {round_obj.name} ===[/bold cyan]\n"
                f"[dim]Veuillez saisir les scores des matchs[/dim]"
            )
        )

    # --------------------------------------------------------------
    # Saisie du score d’un match
    # --------------------------------------------------------------
    def ask_match_result(self, match):
        while True:
            console.print(
                Panel.fit(
                    f"[bold cyan]Résultat du match[/bold cyan]\n\n"
                    f"[white]{match.player1}[/white] vs [white]{match.player2}[/white]\n\n"
                    f"[dim]Scores possibles : 0 / 0.5 / 1[/dim]"
                )
            )

            s1 = console.input(f"Score de {match.player1} : ").replace(",", ".")
            s2 = console.input(f"Score de {match.player2} : ").replace(",", ".")

            try:
                s1 = float(s1)
                s2 = float(s2)

                if s1 in (0, 0.5, 1) and s2 in (0, 0.5, 1):
                    return s1, s2

            except ValueError:
                pass

            console.print("[red]Score invalide. Veuillez entrer 0, 0.5 ou 1.[/red]")
