# views/player_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class PlayerView:
    """
    Vue responsable de toutes les interactions utilisateur concernant les joueurs :
    - saisie
    - validation / modification / annulation
    - affichage
    - suppression
    """

    # --------------------------------------------------------------
    # Saisie sécurisée (annulation possible)
    # --------------------------------------------------------------
    def safe_input(self, message):
        value = console.input(message)
        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée, retour au menu.[/yellow]")
            return None
        return value

    # --------------------------------------------------------------
    # Saisie + validation d’un joueur
    # --------------------------------------------------------------
    def ask_player_info(self):
        """
        Saisie complète d’un joueur avec :
        - récapitulatif
        - valider / modifier / annuler
        """

        while True:
            console.print(Panel.fit("[bold cyan]Création d'un joueur[/bold cyan]"))

            last_name = self.safe_input("Nom : ")
            if last_name is None:
                return None

            first_name = self.safe_input("Prénom : ")
            if first_name is None:
                return None

            birthdate = self.safe_input("Date de naissance (JJ/MM/AAAA) : ")
            if birthdate is None:
                return None

            national_id = self.safe_input("Identifiant national : ")
            if national_id is None:
                return None

            # --- RÉCAPITULATIF ---
            console.print(Panel.fit(
                f"[bold cyan]Vérification des informations[/bold cyan]\n\n"
                f"Nom : {last_name}\n"
                f"Prénom : {first_name}\n"
                f"Date de naissance : {birthdate}\n"
                f"ID National : {national_id}\n"
            ))

            console.print("1. Valider")
            console.print("2. Modifier")
            console.print("3. Annuler\n")

            choice = console.input("[yellow]Votre choix : [/yellow]")

            if choice == "1":
                return {
                    "last_name": last_name,
                    "first_name": first_name,
                    "birthdate": birthdate,
                    "national_id": national_id
                }

            elif choice == "2":
                console.print("[cyan]Modification...[/cyan]\n")

            elif choice == "3":
                console.print("[yellow]Création annulée.[/yellow]")
                return None

            else:
                console.print("[red]Choix invalide.[/red]")

    # --------------------------------------------------------------
    # Confirmation création
    # --------------------------------------------------------------
    def confirm_player_created(self, player):
        console.print(f"[green]Joueur {player.first_name} {player.last_name} créé avec succès ![/green]")

    # --------------------------------------------------------------
    # Confirmation suppression
    # --------------------------------------------------------------
    def confirm_player_deleted(self, player):
        console.print(f"[red]Joueur {player.first_name} {player.last_name} supprimé.[/red]")

    # --------------------------------------------------------------
    # Affichage numéroté
    # --------------------------------------------------------------
    def show_players(self, players):
        table = Table(title="Liste des joueurs")

        table.add_column("N°", style="yellow")
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("ID National", style="magenta")
        table.add_column("Score", style="green")

        for i, p in enumerate(players, start=1):
            table.add_row(str(i), p.last_name, p.first_name, p.national_id, str(p.score))

        console.print(table)
