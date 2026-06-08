# models/tournament.py

from models.round import Round


class Tournament:
    """Modèle représentant un tournoi d'échecs et toutes ses données associées."""

    def __init__(self, name, location, start_date, end_date, description="", number_of_rounds=3):
        """Initialise les attributs principaux d'un tournoi."""
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = int(number_of_rounds)
        self.rounds = []
        self.players = []

    def to_dict(self):
        """Convertit l'objet Tournament en dictionnaire pour TinyDB."""
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            # On s'assure que chaque round appelle sa propre méthode to_dict()
            "rounds": [r.to_dict() if hasattr(r, "to_dict") else r for r in self.rounds],
            "players": self.players
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstruit proprement un objet Tournament et ses sous-objets Rounds depuis TinyDB."""
        if not data:
            return None

        tournament = cls(
            name=data.get("name"),
            location=data.get("location"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            description=data.get("description", ""),
            number_of_rounds=data.get("number_of_rounds", 3)
        )

        # Le FIX : On force la reconstruction des objets Round pour ne pas perdre les attributs temporels
        raw_rounds = data.get("rounds", [])
        tournament.rounds = [Round.from_dict(r) if isinstance(r, dict) else r for r in raw_rounds]

        tournament.players = data.get("players", [])
        return tournament
