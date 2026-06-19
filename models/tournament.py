# models/tournament.py


class Tournament:
    """Modèle représentant un tournoi d'échecs."""

    def __init__(self, name, location, start_date, end_date, description="", number_of_rounds=3):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = 3
        self.rounds = []
        self.players = []

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "number_of_rounds": self.number_of_rounds,
            "rounds": [r.to_dict() if hasattr(r, "to_dict") else r for r in self.rounds],
            "players": self.players
        }

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None

        tournament = cls(
            name=data.get("name"),
            location=data.get("location"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            description=data.get("description", ""),
            number_of_rounds=3
        )
        tournament.rounds = data.get("rounds", [])
        tournament.players = data.get("players", [])
        return tournament
