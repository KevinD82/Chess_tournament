# models/player.py

class Player:
    """
    Modèle représentant un joueur d'échecs.
    Compatible avec TinyDB via to_dict() / from_dict().
    """

    def __init__(self, last_name, first_name, birthdate, national_id, score=0):
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate  # format string "JJ/MM/AAAA"
        self.national_id = national_id  # format AB12345
        self.score = score  # score cumulé dans un tournoi

    # ---------- Sérialisation ----------
    def to_dict(self):
        """Convertit l'objet Player en dictionnaire pour TinyDB."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthdate": self.birthdate,
            "national_id": self.national_id,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data):
        """Recrée un Player depuis un dictionnaire TinyDB."""
        return cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birthdate=data["birthdate"],
            national_id=data["national_id"],
            score=data.get("score", 0),
        )

    # ---------- Méthodes utiles ----------
    def add_points(self, points):
        """Ajoute des points au joueur après un match."""
        self.score += points

    def reset_score(self):
        """Réinitialise le score (utile au début d'un tournoi)."""
        self.score = 0

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id}) - {self.score} pts"
