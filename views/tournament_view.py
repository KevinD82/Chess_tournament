# views/tournament_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class TournamentView:
    """
    Vue responsable de :
    - création d’un tournoi
    - validation / modification / annulation
    - sélection des joueurs
    """

    def safe_input(self, message):
        value = console.input(message)
        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée.[/yellow]")
            return None
        return value

    # --------------------------------------------------------------
    # Saisie + validation d’un tournoi
    # --------------------------------------------------------------
    def ask_tournament_info(self):
        while True:
            console.print(Panel.fit("[bold cyan]Création d'un tournoi[/bold cyan]"))

            name = self.safe_input("Nom : ")
            if name is None:
                return None

            location = self.safe_input("Lieu : ")
            if location is None:
                return None

            start_date = self.safe_input("Date début : ")
            if start_date is None:
                return None

            end_date = self.safe_input("Date fin : ")
            if end_date is None:
                return None

            description = self.safe_input("Description : ")
            if description is None:
                return None

            # --- RÉCAP ---
            console.print(Panel.fit(
                f"[bold cyan]Vérification[/bold cyan]\n\n"
                f"Nom : {name}\n"
                f"Lieu : {location}\n"
                f"Début : {start_date}\n"
                f"Fin : {end_date}\n"
                f"Description : {description}\n"
            ))

            console.print("1. Valider")
            console.print("2. Modifier")
            console.print("3. Annuler\n")

            choice = console.input("[yellow]Votre choix : [/yellow]")

            if choice == "1":
                return {
                    "name": name,
                    "location": location,
                    "start_date": start_date,
                    "end_date": end_date,
                    "description": description,
                }

            elif choice == "2":
                console.print("[cyan]Modification...[/cyan]\n")

            elif choice == "3":
                console.print("[yellow]Création annulée.[/yellow]")
                return None

            else:
                console.print("[red]Choix invalide.[/red]")

    # --------------------------------------------------------------
    # Sélection des joueurs avec validation
    # --------------------------------------------------------------
    def select_players(self, players):
        while True:
            console.print(Panel.fit("[bold cyan]Sélection des joueurs[/bold cyan]"))

            table = Table(title="Joueurs disponibles")
            table.add_column("N°", style="yellow")
            table.add_column("Nom", style="cyan")
            table.add_column("Prénom", style="cyan")
            table.add_column("ID", style="magenta")

            for i, p in enumerate(players, start=1):
                table.add_row(str(i), p.last_name, p.first_name, p.national_id)

            console.print(table)

            raw = self.safe_input("Numéros (ex: 1,3,5) : ")
            if raw is None:
                return None

            try:
                indexes = [int(x.strip()) - 1 for x in raw.split(",")]
                selected = [players[i] for i in indexes]
            except:
                console.print("[red]Format invalide.[/red]")
                continue

            recap = "\n".join(f"- {p.first_name} {p.last_name}" for p in selected)

            console.print(Panel.fit(
                f"[bold cyan]Joueurs sélectionnés[/bold cyan]\n\n{recap}"
            ))

            console.print("1. Valider")
            console.print("2. Modifier")
            console.print("3. Annuler\n")

            choice = console.input("[yellow]Votre choix : [/yellow]")

            if choice == "1":
                return selected
            elif choice == "2":
                console.print("[cyan]Modification...[/cyan]\n")
            elif choice == "3":
                console.print("[yellow]Sélection annulée.[/yellow]")
                return None
            else:
                console.print("[red]Choix invalide.[/red]")
