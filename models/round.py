from datetime import datetime


class Round:
    """Round de tournoi contenant une liste de matchs."""

    def __init__(self, name, matches, start_time=None, end_time=""):
        self.name = name
        self.matches = matches
        self.start_time = start_time if start_time else datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.end_time = end_time

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [m.to_dict() if hasattr(m, "to_dict") else m for m in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return cls(
            name=data.get("name"),
            matches=data.get("matches", []),
            start_time=data.get("start_time"),
            end_time=data.get("end_time", "")
        )
