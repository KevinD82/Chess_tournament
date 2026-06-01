# views/round_view.py

from rich.console import Console
from rich.panel import Panel

console = Console()


class RoundView:

    def safe_input(self, message):
        value = console.input(message)
        if value.lower() in ("echap", "escape", "annuler", "cancel", "q"):
            console.print("[yellow]Saisie annulée.[/yellow]")
            return None
        return value

    def ask_match_result(self, match):
        fields = [
            (f"Score de {match.player1} (0 / 0.5 / 1)", "score1"),
            (f"Score de {match.player2} (0 / 0.5 / 1)", "score2"),
        ]

        data = {"score1": "", "score2": ""}
        index = 0

        while 0 <= index < len(fields):
            label, key = fields[index]

            console.print(Panel.fit(
                f"[bold cyan]Résultat du match[/bold cyan]\n\n"
                f"{match.player1} vs {match.player2}\n"
                f"Champ {index+1}/2 : {label}\n"
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

            try:
                score = float(value.replace(",", "."))
                if score not in (0, 0.5, 1):
                    raise ValueError
            except:
                console.print("[red]Score invalide.[/red]")
                continue

            data[key] = score
            index += 1

        return data["score1"], data["score2"]
