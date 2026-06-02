# database.py

import os
from tinydb import TinyDB, Query

# -------------------------------------------------------------------
# Création automatique du dossier de stockage pour TinyDB
# -------------------------------------------------------------------
DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "db.json")

os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------------------------------------------------
# Initialisation de la base TinyDB
# -------------------------------------------------------------------
db = TinyDB(DB_PATH)

# Tables
players_table = db.table("players")
tournaments_table = db.table("tournaments")

# Queries
PlayerQuery = Query()
TournamentQuery = Query()
