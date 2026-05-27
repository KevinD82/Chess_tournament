# models/tournament.py

from models.round import Round
from models.match import Match
from datetime import datetime
import random


class Tournament:
    """
    Modèle représentant un tournoi d'échecs.
    Contient :
    - nom, lieu, dates
    - nombre de tours (4 par défaut)
    - numéro du tour courant
    - liste des rounds
    - liste des joueurs
    - description
    """

    def __init__(
        self,
        name,
        location,
        start_date,
        end_date,
        players=None,
        rounds=None,
        current_round=0,
        number_of_rounds=4,
        description=""
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.players = players if players is not None else []
        self.rounds = rounds if rounds is not None else []
        self.current_round = current_round
        self.number_of_rounds = number_of_rounds
        self.description = description

    # ---------------------------------------------------------
    #  Génération des paires
    # ---------------------------------------------------------
    def generate_pairs(self):
        """
        Génère les paires pour un nouveau round.
        Respecte :
        - tri par score
        - tirage aléatoire si égalité
        - éviter les matchs déjà joués
        """

        # 1. Trier les joueurs par score (descendant)
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)

        # 2. Mélanger les joueurs ayant le même score
        i = 0
        while i < len(sorted_players) - 1:
            j = i + 1
            if sorted_players[i].score == sorted_players[j].score:
                random.shuffle(sorted_players[i:j+1])
            i += 1

        # 3. Éviter les matchs déjà joués
        pairs = []
        used = set()

        def already_played(p1, p2):
            for rnd in self.rounds:
                for match in rnd.matches:
                    if {match.player1.national_id, match.player2.national_id} == {p1.national_id, p2.national_id}:
                        return True
            return False

        for i in range(0, len(sorted_players), 2):
            p1 = sorted_players[i]

            # Trouver un adversaire disponible
            for j in range(i + 1, len(sorted_players)):
                p2 = sorted_players[j]
                if p2 not in used and not already_played(p1, p2):
                    pairs.append((p1, p2))
                    used.add(p1)
                    used.add(p2)
                    break

        return pairs

    # ---------------------------------------------------------
    #  Création d'un nouveau round
    # ---------------------------------------------------------
    def create_round(self):
        """Crée un nouveau round avec les paires générées."""
        self.current_round += 1
        round_name = f"Round {self.current_round}"

        pairs = self.generate_pairs()
        matches = [Match(p1, p2) for p1, p2 in pairs]

        new_round = Round(round_name, matches)
        self.rounds.append(new_round)

        return new_round

    # ---------------------------------------------------------
    #  Mise à jour des scores après un round
    # ---------------------------------------------------------
    def update_scores(self, round_obj):
        """Met à jour les scores des joueurs après un round."""
        for match in round_obj.matches:
            match.player1.add_points(match.score1)
            match.player2.add_points(match.score2)

    # ---------------------------------------------------------
    #  Sérialisation TinyDB
    # ---------------------------------------------------------
    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "players": [p.national_id for p in self.players],
            "rounds": [r.to_dict() for r in self.rounds],
            "current_round": self.current_round,
            "number_of_rounds": self.number_of_rounds,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data, players_lookup):
        rounds = [
            Round.from_dict(r, players_lookup)
            for r in data["rounds"]
        ]

        players = [players_lookup[p_id] for p_id in data["players"]]

        return cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            players=players,
            rounds=rounds,
            current_round=data["current_round"],
            number_of_rounds=data["number_of_rounds"],
            description=data["description"],
        )

    # ---------------------------------------------------------
    #  Représentation
    # ---------------------------------------------------------
    def __str__(self):
        return f"{self.name} - {self.location} ({self.start_date} → {self.end_date})"
