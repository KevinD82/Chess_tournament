# views/player_view.py

import re
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()


class PlayerView:
    """Gère l'interface utilisateur (affichages et saisies) pour les joueurs."""

    def display_player_menu(self):
        """Affiche le menu de gestion des joueurs et retourne le choix de l'utilisateur."""
        console.print("\n[bold cyan]=== GESTION DES JOUEURS ===[/bold cyan]")
        console.print("1. Créer un joueur")
        console.print("2. Liste des joueurs")
        console.print("3. Supprimer un joueur")
        console.print("0. Retour au menu principal")
        return console.input("\n[bold yellow]Votre choix : [/bold yellow]")

    def ask_player_info(self):
        """Demande, valide et retourne les informations d'un joueur avec confirmation finale.

        Permet à l'utilisateur de recommencer la saisie complète en cas d'erreur.
        """
        # Boucle principale permettant de recommencer tout le formulaire si l'utilisateur refuse la confirmation
        while True:
            console.print("\n[bold cyan]-- Création d'un nouveau joueur --[/bold cyan]")

            # 1. SAISIE DU NOM
            last_name = console.input("Nom de famille : ").strip()
            if not last_name:
                console.print("[red]Le nom ne peut pas être vide.[/red]")
                continue

            # 2. SAISIE DU PRÉNOM
            first_name = console.input("Prénom : ").strip()
            if not first_name:
                console.print("[red]Le prénom ne peut pas être vide.[/red]")
                continue

            # 3. VALIDATION DE LA DATE DE NAISSANCE (Format JJ/MM/AAAA + Limite de 10 ans minimum)
            while True:
                birth_date_str = console.input("Date de naissance (JJ/MM/AAAA) : ").strip()
                try:
                    # Vérifie automatiquement le format, les mois (1-12) et les jours (1-31 selon le mois)
                    birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y")

                    # Calcul dynamique de l'âge de manière exacte
                    today = datetime.today()
                    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

                    if age < 10:
                        console.print("[red]Erreur : Le joueur doit être âgé d'au moins 10 ans.[/red]")
                        continue

                    break  # La date est valide, on sort de la sous-boucle
                except ValueError:
                    console.print("[red]Format ou date invalide. Exemple : 25/12/1995 .[/red]")

            # 4. VALIDATION DE L'ID NATIONAL (2 lettres majuscules suivies de 5 chiffres)
            while True:
                national_id = console.input("Identifiant National d'échecs (ex: AB12345) : ").strip().upper()

                # Expression régulière stricte pour valider la structure requise
                if not re.match(r"^[A-Z]{2}\d{5}$", national_id):
                    console.print("[red]Identifiant invalide ! (AB12345).[/red]")
                    continue

                break  # L'ID est valide, on sort de la sous-boucle

            # --- ÉCRAN DE CONFIRMATION FINALE ---
            console.print("\n[bold yellow]⚠️ Récapitulatif des informations saisies :[/bold yellow]")
            console.print(f" -> [bold]Nom :[/bold] {last_name}")
            console.print(f" -> [bold]Prénom :[/bold] {first_name}")
            console.print(f" -> [bold]Date de naissance :[/bold] {birth_date_str}")
            console.print(f" -> [bold]ID National :[/bold] {national_id}")

            confirmation = console.input("\n[bold magenta]Est-ce correct ? (O/N) : [/bold magenta]").strip().upper()

            if confirmation == "O":
                # Données validées, on renvoie le dictionnaire au contrôleur pour l'insertion
                return {
                    "last_name": last_name,
                    "first_name": first_name,
                    "birthdate": birth_date_str,  # Clé synchronisée avec le modèle Player
                    "national_id": national_id
                }
            else:
                # L'utilisateur demande une correction, on relance la boucle principale
                console.print("[yellow]Saisie annulée. Recommençons depuis le début...[/yellow]\n")

    def show_players(self, players):
        """Prend une liste d'objets joueurs et les affiche dans un tableau Rich structuré."""
        if not players:
            console.print("[yellow]Aucun joueur enregistré pour le moment.[/yellow]")
            return

        table = Table(title="Liste des Joueurs Enregistrés")
        table.add_column("Numéro", justify="center", style="cyan")
        table.add_column("ID National", justify="center", style="magenta")
        table.add_column("Nom", style="green")
        table.add_column("Prénom", style="green")
        table.add_column("Date de Naissance", justify="center")

        for index, player in enumerate(players, start=1):
            table.add_row(
                str(index),
                player.national_id,
                player.last_name,
                player.first_name,
                player.birthdate  # Corrigé : utilise l'attribut exact du modèle sans plantage
            )

        console.print(table)
