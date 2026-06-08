# models/tournament.py

class Tournament:
    def __init__(
        self,
        name,
        location,
        start_date,
        end_date,
        description,
        start_time=None,
        end_time=None,
        players=None,
        rounds=None,
        results=None

    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

        self.start_time = start_time or ""
        self.end_time = end_time or ""

        self.players = players or []
        self.rounds = rounds or []
        self.results = results or []

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "players": self.players,
            "rounds": self.rounds,
            "results": self.results,

        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            location=data.get("location"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            description=data.get("description"),
            players=data.get("players"),
            rounds=data.get("rounds"),
            results=data.get("results"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time")
        )
