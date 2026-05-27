# models/round.py

from datetime import datetime
from models.match import Match


class Round:
    """
    Modèle représentant un round (tour) d'un tournoi.

    Un round contient :
    - un nom (ex : "Round 1")
    - une date/heure de début
    - une date/heure de fin (remplie quand le round est terminé)
    - une liste de matchs (objets Match)

    Ce modèle est utilisé dans Tournament pour structurer la progression du tournoi.
    """

    def __init__(self, name, matches=None, start_time=None, end_time=None):
        """
        Initialise un round.

        name        : nom du round (ex : "Round 1")
        matches     : liste d'objets Match
        start_time  : date/heure de début (string)
        end_time    : date/heure de fin (string ou None)
        """
        self.name = name

        # Si aucune date de début n'est fournie, on utilise l'heure actuelle
        self.start_time = start_time or self._now()

        # end_time reste None tant que le round n'est pas terminé
        self.end_time = end_time

        # matches est une liste d'objets Match
        self.matches = matches if matches is not None else []

    # ----------------------------------------------------------------------
    # Utilitaires internes
    # ----------------------------------------------------------------------
    def _now(self):
        """
        Retourne la date/heure actuelle sous forme de string.
        Format : "JJ/MM/AAAA HH:MM:SS"
        """
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def end_round(self):
        """
        Marque le round comme terminé en enregistrant l'heure de fin.
        Appelé lorsque tous les résultats des matchs ont été saisis.
        """
        self.end_time = self._now()

    # ----------------------------------------------------------------------
    # Sérialisation pour TinyDB
    # ----------------------------------------------------------------------
    def to_dict(self):
        """
        Convertit le round en dictionnaire pour stockage dans TinyDB.

        ⚠️ Important :
        Les matchs sont eux-mêmes convertis en dictionnaires via Match.to_dict().
        """
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "matches": [m.to_dict() for m in self.matches],
        }

    @classmethod
    def from_dict(cls, data, players_lookup):
        """
        Recrée un objet Round à partir d'un dictionnaire TinyDB.

        players_lookup : dict { national_id : Player }
        → permet de reconstruire les objets Match avec les bons joueurs.
        """

        # Reconstruction de chaque match du round
        matches = [
            Match.from_dict(m, players_lookup)
            for m in data["matches"]
        ]

        return cls(
            name=data["name"],
            matches=matches,
            start_time=data["start_time"],
            end_time=data["end_time"],
        )

    # ----------------------------------------------------------------------
    # Représentation textuelle
    # ----------------------------------------------------------------------
    def __str__(self):
        """
        Retourne une représentation lisible du round.
        Exemple :
        "Round 1 (12/05/2024 14:00:00 → en cours)"
        """
        return f"{self.name} ({self.start_time} → {self.end_time or 'en cours'})"
