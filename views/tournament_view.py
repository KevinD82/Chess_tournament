# views/tournament_view.py

from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()


class TournamentView:
    """Affichage des tournois."""

    def display_tournament_menu(self):
        console.print("\n[bold cyan]=== GESTION DES TOURNOIS ===[/bold cyan]")
        console.print("1. Créer un tournoi")
        console.print("2. Liste des tournois")
        console.print("3. Piloter un tournoi")
        console.print("4. Supprimer un tournoi")
        console.print("0. Retour")
        return console.input("\n[bold yellow]Votre choix : [/bold yellow]")

    def display_manage_menu(self, tournament):
        """Affiche le menu de pilotage avec le round actuel et son avancement."""
        console.print(f"\n[bold cyan]=== PILOTAGE : {tournament.name.upper()} ===[/bold cyan]")
        console.print(f"[white]Joueurs sélectionnés : {len(tournament.players)} / 4[/white]")

        total_rounds = tournament.number_of_rounds
        played_rounds = len(tournament.rounds)

        if not tournament.players or len(tournament.players) < 4:
            status_text = "[bold yellow]En attente de la sélection des joueurs[/bold yellow]"
        elif played_rounds == 0:
            status_text = "[bold magenta]Prêt à lancer le Round 1[/bold magenta]"
        else:
            last_round = tournament.rounds[-1]
            if isinstance(last_round, dict):
                has_end_time = bool(last_round.get("end_time"))
                r_name = last_round.get("name", f"Round {played_rounds}")
            else:
                has_end_time = bool(getattr(last_round, "end_time", None))
                r_name = getattr(last_round, "name", f"Round {played_rounds}")

            if has_end_time:
                if played_rounds >= total_rounds:
                    status_text = "[bold green]Tournoi terminé ![/bold green]"
                else:
                    status_text = (
                        f"[bold green]{r_name} terminé[/bold green] → "
                        f"[bold magenta]Prêt à générer le Round {played_rounds + 1}[/bold magenta]"
                    )
            else:
                status_text = f"[bold yellow]{r_name} en cours (Saisie des scores attendue)[/bold yellow]"

        console.print(f"[white]Statut actuel      : {status_text}[/white]")
        console.print("[dim]--------------------------------------------------[/dim]")

        console.print("1. Sélectionner les 4 joueurs participants")
        console.print("2. Générer le prochain Round")
        console.print("3. Saisir les scores du Round actif")
        console.print("0. Retour")
        return console.input("\n[bold yellow]Votre choix : [/bold yellow]")

    def ask_tournament_info(self):
        while True:
            console.print("\n[bold cyan]Création d'un tournoi[/bold cyan]")
            name = console.input("Nom : ").strip()
            if not name:
                console.print("[red]Nom vide.[/red]")
                continue
            location = console.input("Lieu : ").strip()
            if not location:
                console.print("[red]Lieu vide.[/red]")
                continue
            while True:
                start_date_str = console.input("Début (JJ/MM/AAAA) : ").strip()
                try:
                    datetime.strptime(start_date_str, "%d/%m/%Y")
                    break
                except ValueError:
                    console.print("[red]Format de date invalide.[/red]")
            while True:
                end_date_str = console.input("Fin (JJ/MM/AAAA) : ").strip()
                try:
                    datetime.strptime(end_date_str, "%d/%m/%Y")
                    break
                except ValueError:
                    console.print("[red]Format de date invalide.[/red]")
            description = console.input("Description : ").strip()

            console.print("\n[bold yellow]Récapitulatif[/bold yellow]")
            console.print(f"Nom : {name}")
            console.print(f"Lieu : {location}")
            console.print(f"Dates : {start_date_str} → {end_date_str}")
            console.print(f"Description : {description or 'Aucune'}")

            if console.input("\n[green]Confirmer ? (O/N) : [/green]").strip().upper() == "O":
                return {
                    "name": name,
                    "location": location,
                    "start_date": start_date_str,
                    "end_date": end_date_str,
                    "description": description,
                    "number_of_rounds": 3
                }

    def show_tournaments(self, tournaments):
        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré.[/yellow]")
            return

        table = Table(show_header=True, header_style="bold cyan", border_style="dim")
        table.add_column("N°", justify="center")
        table.add_column("Nom")
        table.add_column("Lieu")
        table.add_column("Dates", justify="center")
        table.add_column("Rounds", justify="center")
        table.add_column("Joueurs", justify="center")

        for i, t in enumerate(tournaments, 1):
            table.add_row(
                str(i), t.name, t.location, f"{t.start_date} - {t.end_date}",
                f"{len(t.rounds)} / {t.number_of_rounds}", f"{len(t.players)} / 4"
            )
        console.print(table)

    def select_4_players(self, active_players):
        console.print("\n[bold cyan]=== SÉLECTION DES 4 PARTICIPANTS AU TOURNOI ===[/bold cyan]")
        table = Table(show_header=True, header_style="bold cyan", border_style="dim")
        table.add_column("N°", justify="center")
        table.add_column("ID National", justify="center")
        table.add_column("Nom Complet")
        table.add_column("Statut", justify="center")

        for idx, p in enumerate(active_players, 1):
            status = "[green]Actif[/green]" if getattr(p, "is_active", True) else "[red]Inactif[/red]"
            table.add_row(str(idx), p.national_id, f"{p.last_name} {p.first_name}", status)
        console.print(table)

        selected_ids = []
        for position in range(1, 5):
            while True:
                choice = console.input(
                    f"Sélectionnez le numéro pour le [bold yellow]Joueur {position}[/bold yellow] : "
                ).strip()

                if not choice.isdigit():
                    console.print("[red]Veuillez entrer un nombre valide.[/red]")
                    continue
                idx = int(choice) - 1
                if idx < 0 or idx >= len(active_players):
                    console.print("[red]Numéro invalide, hors liste.[/red]")
                    continue
                chosen_player = active_players[idx]
                if chosen_player.national_id in selected_ids:
                    console.print("[red]Joueur déjà sélectionné.[/red]")
                    continue

                selected_ids.append(chosen_player.national_id)
                console.print(
                    f"[green]Joueur {position} validé : {chosen_player.first_name} "
                    f"{chosen_player.last_name}[/green]\n"
                )
                break
        return selected_ids
