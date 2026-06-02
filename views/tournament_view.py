# views/tournament_view.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class TournamentView:

    # --------------------------------------------------------------
    # Saisie sécurisée
    # --------------------------------------------------------------
    def safe_input(self, message):
        value = console.input(message)
        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée.[/yellow]")
            return None
        return value

    # --------------------------------------------------------------
    # Création d’un tournoi
    # --------------------------------------------------------------
    def ask_tournament_info(self):
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

            if value.strip() == "":
                if index > 0:
                    index -= 1
                    continue
                console.print("[yellow]Déjà au premier champ.[/yellow]")
                continue

            if key in ("start_date", "end_date"):
                digits = "".join(c for c in value if c.isdigit())
                if len(digits) != 8:
                    console.print("[red]Format invalide. Exemple : 01062026[/red]")
                    continue
                value = f"{digits[0:2]}/{digits[2:4]}/{digits[4:8]}"

            data[key] = value
            index += 1

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
    # Affichage des tournois
    # --------------------------------------------------------------
    def show_tournaments(self, tournaments):
        table = Table(title="Liste des tournois")

        table.add_column("N°", style="yellow")
        table.add_column("Nom", style="cyan")
        table.add_column("Lieu", style="cyan")
        table.add_column("Dates", style="magenta")

        for i, t in enumerate(tournaments, start=1):
            table.add_row(
                str(i),
                t.name,
                t.location,
                f"{t.start_date} → {t.end_date}"
            )

        console.print(table)

    # --------------------------------------------------------------
    # Sélection d’un tournoi
    # --------------------------------------------------------------
    def select_tournament(self, tournaments):
        if not tournaments:
            console.print("[red]Aucun tournoi disponible.[/red]")
            return None

        self.show_tournaments(tournaments)

        choice = console.input("Numéro du tournoi (Entrée vide = annuler) : ")

        if choice.strip() == "":
            console.print("[yellow]Sélection annulée.[/yellow]")
            return None

        try:
            index = int(choice) - 1
            return tournaments[index]
        except:
            console.print("[red]Choix invalide.[/red]")
            return None

    # --------------------------------------------------------------
    # Menu de gestion d’un tournoi
    # --------------------------------------------------------------
    def manage_menu(self, tournament):
        console.print(Panel.fit(
            f"[bold cyan]=== Gestion du tournoi : {tournament.name} ===[/bold cyan]\n\n"
            "1. Ajouter des joueurs\n"
            "2. Lancer un round\n"
            "3. Voir les rounds\n"
            "4. Voir le classement final\n"
            "0. Retour"
        ))

        return console.input("Votre choix : ")

    # --------------------------------------------------------------
    # Sélection des joueurs
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

            raw = console.input(
                "[yellow]Numéros des joueurs (ex: 1,3,5) — Entrée vide = annuler : [/yellow]"
            )

            if raw.strip() == "":
                console.print("[yellow]Sélection annulée.[/yellow]")
                return None

            try:
                indexes = [int(x.strip()) - 1 for x in raw.split(",")]
                selected = [players[i] for i in indexes]
            except:
                console.print("[red]Format invalide.[/red]")
                continue

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

    # --------------------------------------------------------------
    # Affichage des rounds
    # --------------------------------------------------------------
    def show_rounds(self, tournament):
        if not tournament.rounds:
            console.print("[yellow]Aucun round joué pour le moment.[/yellow]")
            return

        for r in tournament.rounds:
            console.print(Panel.fit(f"[cyan]{r.name}[/cyan]"))
            for m in r.matches:
                console.print(f"{m.player1} vs {m.player2} → {m.score1} / {m.score2}")
