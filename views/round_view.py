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
                f"[dim]Veuillez saisir les résultats des matchs[/dim]"
            )
        )

    # --------------------------------------------------------------
    # Détermination du vainqueur d’un match (Système 1, N, 2)
    # --------------------------------------------------------------
    def ask_match_result(self, match):
        """
        Demande directement le vainqueur du match.
        Retourne un tuple (score1, score2) automatiquement calculé.
        """
        while True:
            console.print(
                Panel.fit(
                    f"[bold cyan]Résultat du match[/bold cyan]\n\n"
                    f"[white][1] {match.player1}[/white] vs [white][2] {match.player2}[/white]\n\n"
                    f"[yellow]Options : [1] Victoire J1 | [N] Match Nul | [2] Victoire J2[/yellow]"
                )
            )

            choice = console.input("[bold yellow]Votre choix (1, N ou 2) : [/bold yellow]").strip().upper()

            if choice == "1":
                return 1.0, 0.0  # Joueur 1 gagne, Joueur 2 perd
            elif choice == "N" or choice == "0":
                return 0.5, 0.5  # Match nul
            elif choice == "2":
                return 0.0, 1.0  # Joueur 1 perd, Joueur 2 gagne
            else:
                console.print("[red]Choix invalide ! Veuillez taper 1, N, ou 2.[/red]")
