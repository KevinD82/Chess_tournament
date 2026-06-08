# models/round.py

from datetime import datetime


class Round:
    """Modèle représentant un round de tournoi contenant une liste de matchs."""

    def __init__(self, name, matches, start_time=None, end_time=""):
        """Initialise un round avec un nom, ses matchs et ses marqueurs temporels."""
        self.name = name
        self.matches = matches
        # Si aucun start_time n'est fourni, on capture l'instant présent en temps réel
        self.start_time = start_time if start_time else datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.end_time = end_time

    def to_dict(self):
        """Convertit l'objet Round en dictionnaire pour le stockage TinyDB."""
        return {
            "name": self.name,
            "matches": [m.to_dict() if hasattr(m, "to_dict") else m for m in self.matches],
            "start_time": self.start_time,  # Clé cruciale pour sauvegarder l'heure réelle
            "end_time": self.end_time
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruit un objet Round à partir d'un dictionnaire TinyDB."""
        if not data:
            return None
        return cls(
            name=data.get("name"),
            matches=data.get("matches", []),
            start_time=data.get("start_time"),  # Clé cruciale pour relire l'heure réelle
            end_time=data.get("end_time", "")
        )
