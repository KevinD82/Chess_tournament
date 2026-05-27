# models/round.py

from datetime import datetime
from models.match import Match


class Round:
    """
    Modèle représentant un round (tour) d'un tournoi.
    Contient :
    - un nom (ex: "Round 1")
    - une date/heure de début
    - une date/heure de fin
    - une liste de matchs
    """

    def __init__(self, name, matches=None, start_time=None, end_time=None):
        self.name = name
        self.start_time = start_time or self._now()
        self.end_time = end_time  # rempli quand le round est terminé
        self.matches = matches if matches is not None else []

    # ---------- Utilitaires ----------
    def _now(self):
        """Retourne la date/heure actuelle sous forme de string."""
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def end_round(self):
        """Marque le round comme terminé."""
        self.end_time = self._now()

    # ---------- Sérialisation ----------
    def to_dict(self):
        """Convertit le round en dictionnaire pour TinyDB."""
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "matches": [m.to_dict() for m in self.matches],
        }

    @classmethod
    def from_dict(cls, data, players_lookup):
        """
        Recrée un Round depuis un dict.
        players_lookup = dict { national_id: Player }
        """
        matches = [
            Match.from_dict(m, players_lookup)
            for m in data["matches"]
        ]

        return cls(
            name=data["name"],
            matches=matches,
            start_time=data["start_time"],
            end_time=data["end_time"],
        )

    # ---------- Représentation ----------
    def __str__(self):
        return f"{self.name} ({self.start_time} → {self.end_time or 'en cours'})"
