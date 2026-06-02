# models/tournament.py

from models.round import Round


class Tournament:

    def __init__(self, name, location, start_date, end_date, description):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

        self.players = []          # objets Player (non sauvegardés)
        self.players_ids = []      # IDs des joueurs

        self.rounds = []           # objets Round
        self.generated_rounds = []  # liste de paires d'IDs
        self.current_round_index = 0

        self.final_ranking = []    # [(player_id, score), ...]

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "players_ids": self.players_ids,
            "rounds": [r.to_dict() for r in self.rounds],
            "generated_rounds": self.generated_rounds,  # déjà IDs
            "current_round_index": self.current_round_index,
            "final_ranking": self.final_ranking,
        }

    @classmethod
    def from_dict(cls, data):
        t = cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            description=data["description"],
        )

        t.players_ids = data.get("players_ids", [])
        t.rounds = [Round.from_dict(r) for r in data.get("rounds", [])]

        t.generated_rounds = data.get("generated_rounds", [])
        t.current_round_index = data.get("current_round_index", 0)
        t.final_ranking = data.get("final_ranking", [])

        return t
