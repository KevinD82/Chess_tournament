# models/match.py

class Match:
    """
    Modèle représentant un match entre deux joueurs.
    Chaque joueur est stocké avec son score.
    Compatible TinyDB via to_dict() / from_dict().
    """

    def __init__(self, player1, player2, score1=0, score2=0):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    # ---------- Mise à jour des scores ----------
    def set_scores(self, score1, score2):
        """Définit les scores du match."""
        self.score1 = score1
        self.score2 = score2

    # ---------- Sérialisation ----------
    def to_dict(self):
        """
        Convertit le match en dictionnaire.
        On stocke les joueurs via leur identifiant national (clé unique).
        """
        return {
            "player1_id": self.player1.national_id,
            "player2_id": self.player2.national_id,
            "score1": self.score1,
            "score2": self.score2,
        }

    @classmethod
    def from_dict(cls, data, players_lookup):
        """
        Recrée un Match depuis un dict.
        players_lookup = dict { national_id: Player }
        """
        p1 = players_lookup[data["player1_id"]]
        p2 = players_lookup[data["player2_id"]]

        return cls(
            player1=p1,
            player2=p2,
            score1=data["score1"],
            score2=data["score2"],
        )

    # ---------- Représentation ----------
    def __str__(self):
        return (
            f"{self.player1.first_name} {self.player1.last_name} "
            f"({self.score1}) vs "
            f"{self.player2.first_name} {self.player2.last_name} "
            f"({self.score2})"
        )
