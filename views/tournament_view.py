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
