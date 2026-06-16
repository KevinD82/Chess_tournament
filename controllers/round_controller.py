# controllers/round_controller.py

from datetime import datetime
from database import tournaments_table, players_table, TournamentQuery
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


class RoundController:
    """Logique de gestion des rounds et de la saisie des scores."""

    def enter_results(self, tournament):
        """Permet de saisir les scores du round actif avec détection des scores déjà saisis."""
        if not tournament.rounds:
            console.print("[yellow]Aucun round généré pour ce tournoi.[/yellow]")
            return

        # Le round actif est toujours le dernier généré
        active_round = tournament.rounds[-1]

        if isinstance(active_round, dict):
            r_name = active_round.get("name", "Round")
            matches = active_round.get("matches", [])
            is_dict = True
        else:
            r_name = getattr(active_round, "name", "Round")
            matches = getattr(active_round, "matches", [])
            is_dict = False

        # -------------------------------------------------------------------------
        # SÉCURITÉ : Vérification si les scores ont déjà été saisis
        # -------------------------------------------------------------------------
        has_scores = False
        for match in matches:
            if isinstance(match, dict):
                s1 = match.get("score1", 0.0)
                s2 = match.get("score2", 0.0)
            else:
                s1 = getattr(match, "score1", 0.0)
                s2 = getattr(match, "score2", 0.0)

            if s1 > 0.0 or s2 > 0.0:
                has_scores = True
                break

        if has_scores:
            console.print(f"\n[bold yellow]⚠ Attention : Scores de {r_name.upper()}  déjà renseignés ![/bold yellow]")
            confirm = console.input("[bold white]Voulez-vous modifier ? (O/N) : [/bold white]").strip().upper()
            if confirm != "O":
                console.print("[yellow]Modification annulée. Les scores existants ont été conservés.[/yellow]\n")
                return

        # -------------------------------------------------------------------------
        # SUITE : Traitement normal de la saisie
        # -------------------------------------------------------------------------
        players_mapping = {}
        for p_data in players_table.all():
            players_mapping[p_data["national_id"]] = f"{p_data['last_name'].upper()} {p_data['first_name']}"

        console.print(f"\n[bold cyan]=== SAISIE DES SCORES : {r_name.upper()} ===[/bold cyan]\n")

        console.print("[dim]Rappel des commandes :[/dim]")
        console.print(
            "   [bold cyan]1[/bold cyan] : Victoire Joueur 1  |  "
            "[bold yellow]N[/bold yellow] : Match nul  |  "
            "[bold magenta]2[/bold magenta] : Victoire Joueur 2\n"
        )

        for idx, match in enumerate(matches, 1):
            if isinstance(match, dict):
                p1_id = match.get("player1")
                p2_id = match.get("player2")
            else:
                p1_id = getattr(match, "player1")
                p2_id = getattr(match, "player2")

            p1_name = players_mapping.get(p1_id, p1_id)
            p2_name = players_mapping.get(p2_id, p2_id)

            table = Table(show_header=True, header_style="bold white", border_style="cyan", box=box.ROUNDED)
            table.add_column(f"MATCH {idx}", justify="center", style="bold white", width=12)
            table.add_column("Joueur 1 (Touche 1)", justify="right", style="bold cyan", width=25)
            table.add_column("vs", justify="center", style="bold yellow", width=4)
            table.add_column("Joueur 2 (Touche 2)", justify="left", style="bold magenta", width=25)

            table.add_row(f"Affiche {idx}", p1_name, "vs", p2_name)
            console.print(table)

            while True:
                choice = console.input(
                    f"   [bold white]→ Résultat du Match {idx} (1, N ou 2) : [/bold white]"
                ).strip().upper()
                if choice == "1":
                    score1, score2 = 1.0, 0.0
                    break
                elif choice == "N":
                    score1, score2 = 0.5, 0.5
                    break
                elif choice == "2":
                    score1, score2 = 0.0, 1.0
                    break
                else:
                    console.print("   [bold red]⚠ Saisie incorrecte. Veuillez taper 1, N ou 2.[/bold red]")

            if isinstance(match, dict):
                match["score1"] = score1
                match["score2"] = score2
            else:
                match.score1 = score1
                match.score2 = score2

            console.print()

        end_time_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if is_dict:
            active_round["end_time"] = end_time_str
        else:
            active_round.end_time = end_time_str

        serialized_rounds = [
            r.to_dict() if hasattr(r, "to_dict") else r
            for r in tournament.rounds
        ]

        tournaments_table.update(
            {"rounds": serialized_rounds},
            TournamentQuery.name == tournament.name
        )

        console.print(
            f"[bold green]✓ Tous les scores du {r_name} ont été mis à jour "
            f"avec succès à {end_time_str} ![/bold green]\n"
        )
