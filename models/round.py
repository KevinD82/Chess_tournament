# models/round.py

from models.match import Match

class Round:
    """
    Un round contient une liste de matchs.
    """

    def __init__(self, name):
        self.name = name
        self.matches = []

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [m.to_dict() for m in self.matches],
        }

    @classmethod
    def from_dict(cls, data):
        round_obj = cls(name=data["name"])
        round_obj.matches = [Match.from_dict(m) for m in data.get("matches", [])]
        return round_obj
