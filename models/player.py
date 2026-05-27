# models/player.py

class Player:
    """
    Modèle représentant un joueur d'échecs.
    Ce modèle est simple mais essentiel : il sert dans
    - la création de joueurs
    - les tournois
    - les rounds
    - les rapports

    Il est compatible avec TinyDB grâce aux méthodes to_dict() et from_dict().
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
    # Sérialisation pour TinyDB
    # ----------------------------------------------------------------------
    def to_dict(self):
        """
        Convertit l'objet Player en dictionnaire pour stockage dans TinyDB.

        TinyDB ne peut pas stocker directement des objets Python,
        donc on convertit tout en types simples (str, int…).
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
        Recrée un objet Player à partir d'un dictionnaire TinyDB.

        data : dict contenant les champs du joueur
        score : récupéré via data.get() pour éviter une erreur
                si l'ancien format n'avait pas de score.
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
        Utilisé dans la logique de calcul des scores d'un tournoi.
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
