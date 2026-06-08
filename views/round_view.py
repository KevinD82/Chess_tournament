# views/round_view.py

from rich.console import Console
from rich.panel import Panel

console = Console()


class RoundView:
    """Gère l'affichage et les saisies liées aux rounds et aux matchs."""

    def ask_match_result(self, match, players_dict=None):
        """Demande le résultat d'un match avec contrôle de saisie strict et affiche les noms complets."""

        # Récupération sécurisée des identifiants nationaux des deux joueurs
        p1_id = match.player1 if hasattr(match, "player1") else match.get("player1", "Joueur 1")
        p2_id = match.player2 if hasattr(match, "player2") else match.get("player2", "Joueur 2")

        # Conversion de l'ID en "NOM Prénom (ID)" si le dictionnaire des joueurs est disponible
        if players_dict and p1_id in players_dict:
            p1_display = f"{players_dict[p1_id].last_name} {players_dict[p1_id].first_name} ({p1_id})"
        else:
            p1_display = p1_id

        if players_dict and p2_id in players_dict:
            p2_display = f"{players_dict[p2_id].last_name} {players_dict[p2_id].first_name} ({p2_id})"
        else:
            p2_display = p2_id

        # Construction du panneau d'affichage avec Rich
        match_text = (
            f"[bold white][1][/bold white] [green]{p1_display}[/green]\n"
            f"[bold white][2][/bold white] [green]{p2_display}[/green]\n\n"
            f"[bold yellow]Options :[/bold yellow] "
            f"[cyan][1][/cyan] Victoire {p1_id} | [cyan][2][/cyan] Victoire {p2_id} | [cyan][N][/cyan] Match Nul"
        )

        console.print(Panel(match_text, title="Résultat du match", border_style="blue"))

        # Boucle de contrôle de saisie stricte (uniquement 1, 2 ou N)
        while True:
            choice = console.input("[bold yellow]Votre choix (1, 2 ou N) : [/bold yellow]").strip().upper()

            if choice in ["1", "2", "N"]:
                return choice

            console.print("[red]❌ Saisie invalide ! Vous devez obligatoirement entrer 1, 2 ou N.[/red]")
