# models/tournament.py

from models.round import Round


class Tournament:
    """
    Modèle représentant un tournoi d'échecs.
    Stocke uniquement les IDs des joueurs (national_id) pour éviter les doublons.
    """

    def __init__(self, name, location, start_date, end_date, description):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

        # Liste des IDs des joueurs
        self.players = []

        # Liste des rounds (objets Round)
        self.rounds = []

    # --------------------------------------------------------------
    # Conversion → dictionnaire pour TinyDB
    # --------------------------------------------------------------
    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "players": self.players,  # liste d'IDs
            "rounds": [r.to_dict() for r in self.rounds],
        }

    # --------------------------------------------------------------
    # Reconstruction depuis TinyDB
    # --------------------------------------------------------------
    @classmethod
    def from_dict(cls, data):
        """
        Reconstruit un tournoi depuis TinyDB.
        Aucun players_lookup n'est nécessaire.
        """
        tournament = cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            description=data["description"],
        )

        # Liste des IDs des joueurs
        tournament.players = data.get("players", [])

        # Reconstruction des rounds
        tournament.rounds = [
            Round.from_dict(r) for r in data.get("rounds", [])
        ]

        return tournament
