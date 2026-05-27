# views/round_view.py

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Console Rich pour un affichage stylé dans le terminal
console = Console()


class RoundView:
    """
    Vue responsable de l'affichage et de la saisie des résultats des matchs.
    Elle ne contient aucune logique métier : uniquement de l'affichage
    et de la récupération de saisie utilisateur.
    """

    # ------------------------------------------------------------------
    # 1. Saisie sécurisée (annulation possible)
    # ------------------------------------------------------------------
    def safe_input(self, message):
        """
        Demande une saisie utilisateur avec possibilité d'annuler.

        Si l'utilisateur tape :
        - "echap"
        - "escape"
        - "annuler"
        - "cancel"
        - "q"

        Alors la saisie est annulée et la méthode retourne None.
        """
        value = console.input(message)

        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée, retour au menu.[/yellow]")
            return None

        return value

    # ------------------------------------------------------------------
    # 2. Conversion sécurisée en float
    # ------------------------------------------------------------------
    def _safe_float(self, value):
        """
        Convertit une chaîne en float.
        Remplace la virgule par un point pour accepter les formats FR.
        """
        value = value.replace(",", ".")
        return float(value)

    # ------------------------------------------------------------------
    # 3. Validation d’un score
    # ------------------------------------------------------------------
    def _validate_score(self, value):
        """
        Vérifie que le score saisi est valide.
        Scores autorisés : 0, 0.5, 1
        Retourne None si invalide.
        """
        try:
            score = self._safe_float(value)
        except:
            return None

        return score if score in (0, 0.5, 1) else None

    # ------------------------------------------------------------------
    # 4. Saisie du résultat d’un match
    # ------------------------------------------------------------------
    def ask_match_result(self, match):
        """
        Affiche un panneau demandant les scores du match.
        La saisie est répétée tant que le score n’est pas valide.
        L’utilisateur peut annuler à tout moment.
        """

        # Affichage du panneau d'information
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

        # --- Score du joueur 1 ---
        while True:
            raw1 = self.safe_input(
                f"Score de {match.player1.first_name} (0 / 0.5 / 1) : "
            )
            if raw1 is None:
                return None  # Annulation utilisateur

            score1 = self._validate_score(raw1)
            if score1 is not None:
                break

            console.print("[red]Score invalide.[/red]")

        # --- Score du joueur 2 ---
        while True:
            raw2 = self.safe_input(
                f"Score de {match.player2.first_name} (0 / 0.5 / 1) : "
            )
            if raw2 is None:
                return None  # Annulation utilisateur

            score2 = self._validate_score(raw2)
            if score2 is not None:
                break

            console.print("[red]Score invalide.[/red]")

        return score1, score2

    # ------------------------------------------------------------------
    # 5. Confirmation de sauvegarde
    # ------------------------------------------------------------------
    def confirm_results_saved(self):
        """
        Affiche un message confirmant que les résultats ont été enregistrés.
        """
        console.print(
            Panel.fit(
                "[green]Résultats enregistrés ![/green]",
                border_style="green"
            )
        )
