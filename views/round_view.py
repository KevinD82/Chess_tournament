# views/round_view.py

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

class RoundView:

    def safe_input(self, message):
        value = console.input(message)
        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée, retour au menu.[/yellow]")
            return None
        return value

    def _safe_float(self, value):
        value = value.replace(",", ".")
        return float(value)

    def _validate_score(self, value):
        try:
            score = self._safe_float(value)
        except:
            return None
        return score if score in (0, 0.5, 1) else None

    def ask_match_result(self, match):
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

        while True:
            raw1 = self.safe_input(f"Score de {match.player1.first_name} (0 / 0.5 / 1) : ")
            if raw1 is None:
                return None
            score1 = self._validate_score(raw1)
            if score1 is not None:
                break
            console.print("[red]Score invalide.[/red]")

        while True:
            raw2 = self.safe_input(f"Score de {match.player2.first_name} (0 / 0.5 / 1) : ")
            if raw2 is None:
                return None
            score2 = self._validate_score(raw2)
            if score2 is not None:
                break
            console.print("[red]Score invalide.[/red]")

        return score1, score2

    def confirm_results_saved(self):
        console.print(
            Panel.fit(
                "[green]Résultats enregistrés ![/green]",
                border_style="green"
            )
        )
