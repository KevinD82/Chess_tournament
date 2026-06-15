from rich.console import Console
from tinydb import where
from models.match import Match
from database import tournaments_table, players_table, TournamentQuery

console = Console()


class RoundController:
    """Gestion des rounds : saisie des scores avec système 1N2 + modification."""

    def __init__(self):
        pass

    def enter_results(self, tournament):
        """Saisie des scores pour le round en cours."""

        if not tournament.rounds:
            console.print("[yellow]Aucun round à mettre à jour.[/yellow]")
            return

        current_round = tournament.rounds[-1]

        console.print(f"\n[bold cyan]=== Saisie des scores : {current_round.name} ===[/bold cyan]")

        for match in current_round.matches:

            # ---------------------------------------------------------
            # Gestion dict OU objet Match
            # ---------------------------------------------------------
            if isinstance(match, dict):
                player1_id = match.get("player1")
                player2_id = match.get("player2")
                score1 = match.get("score1", 0.0)
                score2 = match.get("score2", 0.0)
            else:
                player1_id = match.player1
                player2_id = match.player2
                score1 = match.score1
                score2 = match.score2

            # Récupération des joueurs
            p1 = players_table.get(where("national_id") == player1_id)
            p2 = players_table.get(where("national_id") == player2_id)

            name1 = f"{p1['first_name']} {p1['last_name']}"
            name2 = f"{p2['first_name']} {p2['last_name']}"

            console.print(f"\nMatch : [bold]{name1}[/bold] vs [bold]{name2}[/bold]")

            # ---------------------------------------------------------
            # Si les scores sont déjà renseignés → demander modification
            # ---------------------------------------------------------
            if float(score1) != 0.0 or float(score2) != 0.0:
                console.print(
                    f"[yellow]Scores déjà enregistrés : {name1} {score1} - {score2} {name2}[/yellow]"
                )
                modify = console.input("Modifier ? (O/N) : ").strip().upper()
                if modify != "O":
                    continue

            # ---------------------------------------------------------
            # Système 1 / N / 2
            # ---------------------------------------------------------
            console.print("[cyan]Entrez le résultat :[/cyan]")
            console.print("1 = victoire joueur 1")
            console.print("N = nul")
            console.print("2 = victoire joueur 2")

            while True:
                result = console.input("Résultat (1/N/2) : ").strip().upper()

                if result == "1":
                    s1, s2 = 1.0, 0.0
                    break
                elif result == "N":
                    s1, s2 = 0.5, 0.5
                    break
                elif result == "2":
                    s1, s2 = 0.0, 1.0
                    break
                else:
                    console.print("[red]Choix invalide.[/red]")

            # Mise à jour des scores
            if isinstance(match, dict):
                match["score1"] = s1
                match["score2"] = s2
            else:
                match.score1 = s1
                match.score2 = s2

        # Sauvegarde en base
        tournaments_table.update(
            {
                "rounds": [
                    r.to_dict() if hasattr(r, "to_dict") else r
                    for r in tournament.rounds
                ]
            },
            TournamentQuery.name == tournament.name
        )

        console.print("\n[green]Scores enregistrés avec succès ![/green]")
