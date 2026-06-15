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
        console.print("3. Ajouter des joueurs à un tournoi")
        console.print("4. Piloter un tournoi")
        console.print("5. Supprimer un tournoi")
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

            today = datetime.now()

            while True:
                start_date_str = console.input("Début (JJ/MM/AAAA) : ").strip()
                try:
                    start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
                    if start_date.date() < today.date():
                        console.print("[red]Date antérieure à aujourd'hui.[/red]")
                        continue
                    break
                except ValueError:
                    console.print("[red]Format invalide.[/red]")

            while True:
                end_date_str = console.input("Fin (JJ/MM/AAAA) : ").strip()
                try:
                    end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
                    if end_date.date() < start_date.date():
                        console.print("[red]Fin avant début.[/red]")
                        continue
                    break
                except ValueError:
                    console.print("[red]Format invalide.[/red]")

            description = console.input("Description (optionnel) : ").strip()

            console.print("\n[bold yellow]Récapitulatif[/bold yellow]")
            console.print(f"Nom : {name}")
            console.print(f"Lieu : {location}")
            console.print(f"Dates : {start_date_str} → {end_date_str}")
            console.print(f"Description : {description or 'Aucune'}")

            if console.input("[green]Confirmer ? (O/N) : [/green]").strip().upper() == "O":
                return {
                    "name": name,
                    "location": location,
                    "start_date": start_date_str,
                    "end_date": end_date_str,
                    "description": description
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

        for i, t in enumerate(tournaments, 1):
            total = t.number_of_rounds
            played = len(t.rounds)
            table.add_row(
                str(i),
                t.name,
                t.location,
                f"{t.start_date} → {t.end_date}",
                f"{played}/{total}"
            )

        console.print(table)

    def select_tournament(self, tournaments):
        self.show_tournaments(tournaments)
        choice = console.input("\nNuméro du tournoi : ").strip()

        if not choice.isdigit():
            console.print("[red]Veuillez entrer un numéro valide.[/red]")
            return None

        index = int(choice) - 1
        if index < 0 or index >= len(tournaments):
            console.print("[red]Numéro hors liste.[/red]")
            return None

        return tournaments[index]

    # ---------------------------------------------------------
    # SÉLECTION GUIDÉE DES 4 JOUEURS
    # ---------------------------------------------------------
    def select_players(self, players):
        console.print("\n[bold cyan]Sélection des joueurs pour le tournoi[/bold cyan]")

        table = Table(show_header=True, header_style="bold cyan", border_style="dim")
        table.add_column("N°", justify="center")
        table.add_column("Nom")
        table.add_column("National ID", justify="center")

        for i, p in enumerate(players, 1):
            table.add_row(
                str(i),
                f"{p['first_name']} {p['last_name']}",
                p["national_id"]
            )

        console.print(table)

        selected = []
        used_indexes = set()

        for n in range(1, 5):
            while True:
                choice = console.input(f"Numéro du joueur {n} : ").strip()

                if not choice.isdigit():
                    console.print("[red]Veuillez entrer un numéro valide.[/red]")
                    continue

                index = int(choice) - 1

                if index < 0 or index >= len(players):
                    console.print("[red]Numéro hors liste.[/red]")
                    continue

                if index in used_indexes:
                    console.print("[red]Ce joueur est déjà sélectionné ![/red]")
                    continue

                used_indexes.add(index)
                selected.append(players[index])
                break

        return selected
