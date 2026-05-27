# models/match.py

class Match:
    """
    Modèle représentant un match entre deux joueurs.
    Un match contient :
    - deux joueurs (player1, player2)
    - deux scores (score1, score2)

    Ce modèle est utilisé dans les rounds d’un tournoi.
    Il est compatible avec TinyDB grâce aux méthodes to_dict() et from_dict().
    """

    def __init__(self, player1, player2, score1=0, score2=0):
        """
        Initialise un match entre deux joueurs.

        player1 / player2 : objets Player
        score1 / score2   : scores attribués à chaque joueur (0, 0.5 ou 1)
        """
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    # ----------------------------------------------------------------------
    # Mise à jour des scores
    # ----------------------------------------------------------------------
    def set_scores(self, score1, score2):
        """
        Met à jour les scores du match.
        Utilisé lors de la saisie des résultats dans RoundController.
        """
        self.score1 = score1
        self.score2 = score2

    # ----------------------------------------------------------------------
    # Sérialisation pour TinyDB
    # ----------------------------------------------------------------------
    def to_dict(self):
        """
        Convertit le match en dictionnaire pour stockage dans TinyDB.

        ⚠️ Important :
        On ne stocke PAS directement les objets Player,
        mais uniquement leur identifiant national (clé unique).
        Cela permet de reconstruire les joueurs plus tard via players_lookup.
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
        Recrée un objet Match à partir d’un dictionnaire TinyDB.

        players_lookup : dict { national_id : Player }
        → permet de retrouver les objets Player correspondants.

        Exemple :
        players_lookup["FR123"] → Player(...)
        """
        p1 = players_lookup[data["player1_id"]]
        p2 = players_lookup[data["player2_id"]]

        return cls(
            player1=p1,
            player2=p2,
            score1=data["score1"],
            score2=data["score2"],
        )

    # ----------------------------------------------------------------------
    # Représentation textuelle (utile pour debug ou affichage simple)
    # ----------------------------------------------------------------------
    def __str__(self):
        """
        Retourne une représentation lisible du match.
        Exemple :
        "Alice Dupont (1) vs Bob Martin (0)"
        """
        return (
            f"{self.player1.first_name} {self.player1.last_name} "
            f"({self.score1}) vs "
            f"{self.player2.first_name} {self.player2.last_name} "
            f"({self.score2})"
        )
