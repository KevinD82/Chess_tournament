# models/match.py

class Match:
    """
    Un match oppose deux joueurs (stockés par leur ID national).
    """

    def __init__(self, player1, player2, score1=0, score2=0):
        self.player1 = player1  # national_id (string)
        self.player2 = player2  # national_id (string)
        self.score1 = score1
        self.score2 = score2

    def to_dict(self):
        return {
            "player1": self.player1,
            "player2": self.player2,
            "score1": self.score1,
            "score2": self.score2,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            player1=data["player1"],
            player2=data["player2"],
            score1=data.get("score1", 0),
            score2=data.get("score2", 0),
        )
