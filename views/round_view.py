# views/round_view.py

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

class RoundView:

    # ---------------------------------------------------------
    #  Convertisseur sécurisé (accepte virgule ou point)
    # ---------------------------------------------------------
    def _safe_float(self, value):
        """Convertit proprement un input en float, accepte virgule ou point."""
        value = value.replace(",", ".")
        return float(value)

    # ---------------------------------------------------------
    #  Validation stricte des scores (0, 0.5, 1)
    # ---------------------------------------------------------
    def _validate_score(self, value):
        try:
            score = self._safe_float(value)
        except ValueError:
            return None

        if score in (0, 0.5, 1):
            return score
        return None

    # ---------------------------------------------------------
    #  Demande du résultat d’un match
    # ---------------------------------------------------------
    def ask_match_result(self, match):
        console.print(
            Panel.fit(
                Text(
                    f"Résultat du match\n"
                    f"{match.player1.first_name} {match.player1.last_name} "
                    f"vs "
                    f"{match.player2.first_name} {match.player2.last_name}",
                    justify="center",
                    style="bold cyan"
                )
            )
        )

        # Score joueur 1
        while True:
            raw1 = console.input(
                f"[yellow]Score de {match.player1.first_name} (0 / 0.5 / 1) : [/yellow]"
            )
            score1 = self._validate_score(raw1)
            if score1 is not None:
                break
            console.print("[red]Score invalide. Entrez 0, 0.5 ou 1.[/red]")

        # Score joueur 2
        while True:
            raw2 = console.input(
                f"[yellow]Score de {match.player2.first_name} (0 / 0.5 / 1) : [/yellow]"
            )
            score2 = self._validate_score(raw2)
            if score2 is not None:
                break
            console.print("[red]Score invalide. Entrez 0, 0.5 ou 1.[/red]")

        return score1, score2

    # ---------------------------------------------------------
    #  Confirmation
    # ---------------------------------------------------------
    def confirm_results_saved(self):
        console.print(
            Panel.fit(
                "[green]Les résultats du round ont été enregistrés avec succès ![/green]",
                border_style="green"
            )
        )
