# models/player.py

class Player:
    """
    Modèle représentant un joueur d'échecs.
    Ce modèle sert dans
    - la création de joueurs
    - les tournois
    - les rounds
    - les rapports

    Il contient les informations de base d'un joueur :
    - nom de famille
    - prénom
    - date de naissance
    - identifiant national
    - score (cumulé dans un tournoi)
    """

    def __init__(self, last_name, first_name, birthdate, national_id, score=0):
        """
        Initialise un joueur.

        last_name   : nom de famille
        first_name  : prénom
        birthdate   : date de naissance (format JJ/MM/AAAA)
        national_id : identifiant unique du joueur (clé primaire logique)
        score       : score cumulé dans un tournoi (0 par défaut)
        """
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.national_id = national_id
        self.score = score

    # ----------------------------------------------------------------------
    # Sérialisation
    # ----------------------------------------------------------------------
    def to_dict(self):
        """
        Convertit l'objet en dictionnaire pour stockage dans TinyDB.
        """
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthdate": self.birthdate,
            "national_id": self.national_id,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Recrée un objet à partir d'un dictionnaire TinyDB.
        """
        return cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birthdate=data["birthdate"],
            national_id=data["national_id"],
            score=data.get("score", 0),
        )

    # ----------------------------------------------------------------------
    # Méthodes utiles pour la logique métier
    # ----------------------------------------------------------------------
    def add_points(self, points):
        """
        Ajoute des points au joueur après un match.
            points : nombre de points à ajouter (1 pour victoire, 0.5 pour nul, 0 pour défaite)
        """
        self.score += points

    def reset_score(self):
        """
        Réinitialise le score du joueur.
        Utile lorsqu'un joueur participe à un nouveau tournoi.
        """
        self.score = 0

    # ----------------------------------------------------------------------
    # Représentation textuelle (utile pour debug et affichage simple)
    # ----------------------------------------------------------------------
    def __str__(self):
        """
        Retourne une représentation lisible du joueur.
        Exemple : "Alice Dupont (FR12345) - 2 pts"
        """
        return f"{self.first_name} {self.last_name} ({self.national_id}) - {self.score} pts"
