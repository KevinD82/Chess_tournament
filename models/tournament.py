# models/tournament.py

from models.round import Round
from models.match import Match
from datetime import datetime
import random


class Tournament:
    """
    Modèle représentant un tournoi d'échecs.

    Un tournoi contient :
    - nom, lieu, dates
    - nombre total de rounds (4 par défaut)
    - numéro du round courant
    - liste des rounds (objets Round)
    - liste des joueurs (objets Player)
    - description

    Ce modèle contient toute la logique métier du tournoi :
    - génération des paires (algorithme suisse simplifié)
    - création des rounds
    - mise à jour des scores
    - sérialisation TinyDB
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

        # Liste des joueurs participant au tournoi
        self.players = players if players is not None else []

        # Liste des rounds déjà joués
        self.rounds = rounds if rounds is not None else []

        # Round en cours (0 = aucun round encore créé)
        self.current_round = current_round

        # Nombre total de rounds prévus
        self.number_of_rounds = number_of_rounds

        # Description libre du tournoi
        self.description = description

    # ----------------------------------------------------------------------
    # 1. Génération des paires (algorithme suisse simplifié)
    # ----------------------------------------------------------------------
    def generate_pairs(self):
        """
        Génère les paires pour un nouveau round.

        Règles appliquées :
        - tri des joueurs par score décroissant
        - mélange aléatoire des joueurs ayant le même score
        - éviter les matchs déjà joués dans les rounds précédents
        """

        # 1. Trier les joueurs par score (du meilleur au moins bon)
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)

        # 2. Mélanger les joueurs ayant le même score
        #    Cela évite que les mêmes joueurs se rencontrent toujours
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
            """
            Vérifie si p1 et p2 se sont déjà affrontés dans un round précédent.
            """
            for rnd in self.rounds:
                for match in rnd.matches:
                    if {match.player1.national_id, match.player2.national_id} == {
                        p1.national_id, p2.national_id
                    }:
                        return True
            return False

        # Parcours des joueurs deux par deux
        for i in range(0, len(sorted_players), 2):
            p1 = sorted_players[i]

            # Trouver un adversaire disponible
            for j in range(i + 1, len(sorted_players)):
                p2 = sorted_players[j]

                # p2 doit être libre et ne pas avoir déjà joué contre p1
                if p2 not in used and not already_played(p1, p2):
                    pairs.append((p1, p2))
                    used.add(p1)
                    used.add(p2)
                    break

        return pairs

    # ----------------------------------------------------------------------
    # 2. Création d’un nouveau round
    # ----------------------------------------------------------------------
    def create_round(self):
        """
        Crée un nouveau round :
        - incrémente le numéro du round
        - génère les paires
        - crée les matchs
        - crée un objet Round
        - ajoute le round à la liste
        """
        self.current_round += 1
        round_name = f"Round {self.current_round}"

        # Génération des paires selon l’algorithme suisse
        pairs = self.generate_pairs()

        # Création des matchs
        matches = [Match(p1, p2) for p1, p2 in pairs]

        # Création du round
        new_round = Round(round_name, matches)
        self.rounds.append(new_round)

        return new_round

    # ----------------------------------------------------------------------
    # 3. Mise à jour des scores après un round
    # ----------------------------------------------------------------------
    def update_scores(self, round_obj):
        """
        Met à jour les scores des joueurs après un round.

        Chaque match contient :
        - match.score1
        - match.score2

        On ajoute ces points aux joueurs correspondants.
        """
        for match in round_obj.matches:
            match.player1.add_points(match.score1)
            match.player2.add_points(match.score2)

    # ----------------------------------------------------------------------
    # 4. Sérialisation TinyDB
    # ----------------------------------------------------------------------
    def to_dict(self):
        """
        Convertit le tournoi en dictionnaire pour TinyDB.

        ⚠️ Important :
        - On stocke les joueurs via leur national_id
        - On stocke les rounds via Round.to_dict()
        """
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
        """
        Recrée un objet Tournament depuis un dict TinyDB.

        players_lookup : dict { national_id : Player }
        → permet de reconstruire les objets Player et Match
        """

        # Reconstruction des rounds
        rounds = [
            Round.from_dict(r, players_lookup)
            for r in data["rounds"]
        ]

        # Reconstruction des joueurs
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

    # ----------------------------------------------------------------------
    # 5. Représentation textuelle
    # ----------------------------------------------------------------------
    def __str__(self):
        """
        Représentation lisible du tournoi.
        Exemple :
        "Open de Lille - Lille (12/05/2024 → 14/05/2024)"
        """
        return f"{self.name} - {self.location} ({self.start_date} → {self.end_date})"
