# views/tournament_view.py

from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()


class TournamentView:
    """Gère l'interface utilisateur (affichages et saisies) pour les tournois."""

    def display_tournament_menu(self):
        """Affiche le menu de gestion des tournois et retourne le choix de l'utilisateur."""
        console.print("\n[bold cyan]=== GESTION DES TOURNOIS ===[/bold cyan]")
        console.print("1. Créer un nouveau tournoi")
        console.print("2. Liste des tournois")
        console.print("3. Piloter un tournoi en cours (Rounds & Scores)")
        console.print("4. Supprimer un tournoi")
        console.print("0. Retour au menu principal")
        return console.input("\n[bold yellow]Votre choix : [/bold yellow]")

    def ask_tournament_info(self):
        """Demande, valide et retourne les informations d'un tournoi avec confirmation finale.

        Permet à l'utilisateur de recommencer la saisie complète en cas d'erreur.
        """
        while True:
            console.print("\n[bold cyan]-- Création d'un nouveau tournoi --[/bold cyan]")

            # 1. SAISIE DU NOM
            name = console.input("Nom du tournoi : ").strip()
            if not name:
                console.print("[red]Le nom du tournoi ne peut pas être vide.[/red]")
                continue

            # 2. SAISIE DU LIEU
            location = console.input("Lieu : ").strip()
            if not location:
                console.print("[red]Le lieu ne peut pas être vide.[/red]")
                continue

            # Définition de la date du jour (Nous sommes en 2026)
            today = datetime.now()

            # 3. VALIDATION DE LA DATE DE DÉBUT
            while True:
                start_date_str = console.input("Date de début (JJ/MM/AAAA) : ").strip()
                try:
                    start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
                    if start_date.date() < today.date():
                        console.print(
                            "[red]Erreur : La date de début ne peut pas être antérieure à aujourd'hui.[/red]"
                        )
                        continue
                    break
                except ValueError:
                    console.print("[red]Format de date invalide (JJ/MM/AAAA).[/red]")

            # 4. VALIDATION DE LA DATE DE FIN
            while True:
                end_date_str = console.input("Date de fin (JJ/MM/AAAA) : ").strip()
                try:
                    end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
                    if end_date.date() < start_date.date():
                        console.print("[red]Attention : date antérieure à la date de début.[/red]")
                        continue
                    break
                except ValueError:
                    console.print("[red]Format de date invalide (JJ/MM/AAAA).[/red]")

            # 5. SAISIE DE LA DESCRIPTION
            description = console.input("Description / Notes (Optionnel) : ").strip()

            # --- ÉCRAN DE CONFIRMATION FINALE ---
            console.print("\n[bold yellow]⚠️ Récapitulatif des informations saisies :[/bold yellow]")
            console.print(f" -> [bold]Nom :[/bold] {name}")
            console.print(f" -> [bold]Lieu :[/bold] {location}")
            console.print(f" -> [bold]Dates :[/bold] Du {start_date_str} au {end_date_str}")
            console.print(f" -> [bold]Description :[/bold] {description if description else 'Aucune'}")

            confirmation = console.input("\n[bold magenta]Est-ce correct ? (O/N) : [/bold magenta]").strip().upper()

            if confirmation == "O":
                return {
                    "name": name,
                    "location": location,
                    "start_date": start_date_str,
                    "end_date": end_date_str,
                    "description": description
                }
            else:
                console.print("[yellow]Saisie annulée. Recommençons depuis le début...[/yellow]\n")

    def show_tournaments(self, tournaments):
        """Prend une liste d'objets tournois et les affiche dans un tableau Rich structuré."""
        if not tournaments:
            console.print("[yellow]Aucun tournoi enregistré pour le moment.[/yellow]")
            return

        table = Table(title="Liste des Tournois")
        table.add_column("Numéro", justify="center", style="cyan")
        table.add_column("Nom du Tournoi", style="green")
        table.add_column("Lieu", style="magenta")
        table.add_column("Dates (Début - Fin)", justify="center")
        table.add_column("Statut / Rounds", justify="center")

        for index, tournament in enumerate(tournaments, start=1):
            # CORRECTION E128 : Alignement visuel propre et indenté suivant la PEP 8
            total_rounds = getattr(
                tournament, "number_of_rounds", getattr(
                    tournament, "num_rounds", getattr(
                        tournament, "total_rounds", 4
                    )
                )
            )

            rounds_list = getattr(tournament, "rounds", [])
            rounds_count = f"{len(rounds_list)}/{total_rounds}"

            table.add_row(
                str(index),
                tournament.name,
                tournament.location,
                f"{tournament.start_date} au {tournament.end_date}",
                f"En cours ({rounds_count})"
            )

        console.print(table)
