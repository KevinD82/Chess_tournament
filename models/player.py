class Player:
    """Modèle représentant un joueur d'échecs."""

    def __init__(self, last_name, first_name, birthdate, national_id, score=0):
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.national_id = national_id
        self.score = score

    def to_dict(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthdate": self.birthdate,
            "national_id": self.national_id,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birthdate=data["birthdate"],
            national_id=data["national_id"],
            score=data.get("score", 0),
        )

    def add_points(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id}) - {self.score} pts"
