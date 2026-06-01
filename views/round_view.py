# views/round_view.py

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


class RoundView:
    """
    Vue responsable de la saisie des scores :
    - validation
    - modification
    - annulation
    """

    def safe_input(self, message):
        value = console.input(message)
        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée.[/yellow]")
            return None
        return value

    def _safe_float(self, value):
        return float(value.replace(",", "."))

    def _validate_score(self, value):
        try:
            score = self._safe_float(value)
        except:
            return None
        return score if score in (0, 0.5, 1) else None

    # --------------------------------------------------------------
    # Saisie + validation des scores
    # --------------------------------------------------------------
    def ask_match_result(self, match):
        while True:
            console.print(
                Panel.fit(
                    Text(
                        f"Résultat du match\n"
                        f"{match.player1.first_name} {match.player1.last_name} vs "
                        f"{match.player2.first_name} {match.player2.last_name}",
                        justify="center",
                        style="bold cyan"
                    )
                )
            )

            raw1 = self.safe_input(f"Score {match.player1.first_name} : ")
            if raw1 is None:
                return None
            score1 = self._validate_score(raw1)
            if score1 is None:
                console.print("[red]Score invalide.[/red]")
                continue

            raw2 = self.safe_input(f"Score {match.player2.first_name} : ")
            if raw2 is None:
                return None
            score2 = self._validate_score(raw2)
            if score2 is None:
                console.print("[red]Score invalide.[/red]")
                continue

            console.print(Panel.fit(
                f"[bold cyan]Vérification[/bold cyan]\n\n"
                f"{match.player1.first_name} : {score1}\n"
                f"{match.player2.first_name} : {score2}\n"
            ))

            console.print("1. Valider")
            console.print("2. Modifier")
            console.print("3. Annuler\n")

            choice = console.input("[yellow]Votre choix : [/yellow]")

            if choice == "1":
                return score1, score2
            elif choice == "2":
                console.print("[cyan]Modification...[/cyan]\n")
            elif choice == "3":
                console.print("[yellow]Saisie annulée.[/yellow]")
                return None
            else:
                console.print("[red]Choix invalide.[/red]")
