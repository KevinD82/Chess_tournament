# models/tournament.py

class Tournament:
    def __init__(self, name, location, start_date, end_date, description,
                 players=None, rounds=None, results=None):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.players = players or []
        self.rounds = rounds or []
        self.results = results or {}

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "players": self.players,
            "rounds": self.rounds,
            "results": self.results,
        }

    @staticmethod
    def from_dict(data):
        return Tournament(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            description=data["description"],
            players=data.get("players", []),
            rounds=data.get("rounds", []),
            results=data.get("results", {}),
        )
