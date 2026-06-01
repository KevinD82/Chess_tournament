# views/tournament_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class TournamentView:

    # --------------------------------------------------------------
    # Saisie sécurisée (annulation possible)
    # --------------------------------------------------------------
    def safe_input(self, message):
        value = console.input(message)
        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée.[/yellow]")
            return None
        return value

    # --------------------------------------------------------------
    # Saisie intelligente d’un tournoi
    # --------------------------------------------------------------
    def ask_tournament_info(self):
        """
        Saisie simple :
        - Entrée valide
        - Entrée vide = revenir au champ précédent
        """

        fields = [
            ("Nom du tournoi", "name"),
            ("Lieu", "location"),
            ("Date de début (JJ/MM/AAAA)", "start_date"),
            ("Date de fin (JJ/MM/AAAA)", "end_date"),
            ("Description", "description"),
        ]

        data = {key: "" for _, key in fields}
        index = 0

        while 0 <= index < len(fields):
            label, key = fields[index]

            console.print(Panel.fit(
                f"[bold cyan]Création d'un tournoi[/bold cyan]\n\n"
                f"Champ {index+1}/{len(fields)} : {label}\n"
                f"Valeur actuelle : [yellow]{data[key] or '(vide)'}[/yellow]\n"
                f"[dim]Entrée vide = revenir au champ précédent[/dim]"
            ))

            value = console.input(f"{label} : ")

            # Retour arrière
            if value.strip() == "":
                if index > 0:
                    index -= 1
                    continue
                console.print("[yellow]Déjà au premier champ.[/yellow]")
                continue

            # Formatage automatique des dates
            if key in ("start_date", "end_date"):
                digits = "".join(c for c in value if c.isdigit())
                if len(digits) != 8:
                    console.print("[red]Format invalide. Exemple : 01062026[/red]")
                    continue
                value = f"{digits[0:2]}/{digits[2:4]}/{digits[4:8]}"

            data[key] = value
            index += 1

        # Récapitulatif
        console.print(Panel.fit(
            f"[bold cyan]Vérification du tournoi[/bold cyan]\n\n"
            f"Nom : {data['name']}\n"
            f"Lieu : {data['location']}\n"
            f"Début : {data['start_date']}\n"
            f"Fin : {data['end_date']}\n"
            f"Description : {data['description']}\n"
        ))

        confirm = console.input("Valider ? (o/N) : ").lower()
        if confirm == "o":
            return data

        console.print("[yellow]Création annulée.[/yellow]")
        return None

    # --------------------------------------------------------------
    # Sélection des joueurs pour un tournoi
    # --------------------------------------------------------------
    def select_players(self, players):
        """
        Affiche la liste des joueurs et permet d'en sélectionner plusieurs.
        Entrée vide = annuler
        """

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

            raw = console.input(
                "[yellow]Numéros des joueurs (ex: 1,3,5) — Entrée vide = annuler : [/yellow]"
            )

            # Annulation
            if raw.strip() == "":
                console.print("[yellow]Sélection annulée.[/yellow]")
                return None

            try:
                indexes = [int(x.strip()) - 1 for x in raw.split(",")]
                selected = [players[i] for i in indexes]
            except Exception:
                console.print("[red]Format invalide.[/red]")
                continue

            # Récapitulatif
            recap = "\n".join(
                f"- {p.first_name} {p.last_name} ({p.national_id})"
                for p in selected
            )

            console.print(Panel.fit(
                f"[bold cyan]Joueurs sélectionnés[/bold cyan]\n\n{recap}"
            ))

            confirm = console.input("Valider ? (o/N) : ").lower()
            if confirm == "o":
                return selected
