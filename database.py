# database.py

"""
Module de gestion de la base de données TinyDB.

Ce fichier centralise :
- la création du dossier de stockage,
- l'initialisation de la base,
- la déclaration des tables,
- la création des objets Query.

Il sert de point d'accès unique à la base pour tout le projet.
"""

import os
from tinydb import TinyDB, Query

# Dossier et fichier de stockage
DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "db.json")

# Création automatique du dossier si nécessaire
os.makedirs(DATA_DIR, exist_ok=True)

# Initialisation de la base TinyDB
db = TinyDB(DB_PATH)

# Tables utilisées dans l'application
players_table = db.table("players")
tournaments_table = db.table("tournaments")

# Objets Query pour effectuer des recherches
PlayerQuery = Query()
TournamentQuery = Query()
