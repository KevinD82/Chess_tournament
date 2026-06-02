# views/player_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class PlayerView:

    def safe_input(self, message):
        value = console.input(message)
        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée.[/yellow]")
            return None
        return value

    def ask_player_info(self):
        """
        Saisie simple :
        - Entrée valide
        - Entrée vide = revenir au champ précédent
        """

        fields = [
            ("Nom", "last_name"),
            ("Prénom", "first_name"),
            ("Date de naissance (JJ/MM/AAAA)", "birthdate"),
            ("Identifiant national (2 lettres + 5 chiffres)", "national_id"),
        ]

        data = {key: "" for _, key in fields}
        index = 0

        while 0 <= index < len(fields):
            label, key = fields[index]

            console.print(Panel.fit(
                f"[bold cyan]Création d'un joueur[/bold cyan]\n\n"
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

            # Validation date
            if key == "birthdate":
                digits = "".join(c for c in value if c.isdigit())
                if len(digits) != 8:
                    console.print("[red]Format invalide. Exemple : 01062026[/red]")
                    continue
                value = f"{digits[0:2]}/{digits[2:4]}/{digits[4:8]}"

            # Validation ID
            if key == "national_id":
                letters = "".join(c for c in value if c.isalpha()).upper()
                digits = "".join(c for c in value if c.isdigit())
                if len(letters) != 2 or len(digits) != 5:
                    console.print("[red]Format invalide. Exemple : AB12345[/red]")
                    continue
                value = letters + digits

            data[key] = value
            index += 1

        # Récapitulatif
        console.print(Panel.fit(
            f"[bold cyan]Vérification[/bold cyan]\n\n"
            f"Nom : {data['last_name']}\n"
            f"Prénom : {data['first_name']}\n"
            f"Date : {data['birthdate']}\n"
            f"ID : {data['national_id']}\n"
        ))

        confirm = console.input("Valider ? (o/N) : ").lower()
        if confirm == "o":
            return data

        console.print("[yellow]Création annulée.[/yellow]")
        return None

    # --------------------------------------------------------------
    # Affichage numéroté des joueurs
    # --------------------------------------------------------------
    def show_players(self, players):
        table = Table(title="Liste des joueurs")

        table.add_column("N°", style="yellow")
        table.add_column("Nom", style="cyan")
        table.add_column("Prénom", style="cyan")
        table.add_column("ID National", style="magenta")
        table.add_column("Score", style="green")

        for i, p in enumerate(players, start=1):
            table.add_row(
                str(i),
                p.last_name,
                p.first_name,
                p.national_id,
                str(p.score)
            )

        console.print(table)

    # --------------------------------------------------------------
    # Confirmation de création d'un joueur
    # --------------------------------------------------------------
    def confirm_player_created(self, player):
        console.print(
            Panel.fit(
                f"[green]Joueur créé avec succès ![/green]\n\n"
                f"{player.first_name} {player.last_name}\n"
                f"ID : {player.national_id}\n"
                f"Date de naissance : {player.birthdate}"
            )
        )

    # --------------------------------------------------------------
    # Confirmation de suppression d'un joueur
    # --------------------------------------------------------------
    def confirm_player_deleted(self, player):
        console.print(
            Panel.fit(
                f"[red]Joueur supprimé[/red]\n\n"
                f"{player.first_name} {player.last_name}\n"
                f"ID : {player.national_id}"
            )
        )
