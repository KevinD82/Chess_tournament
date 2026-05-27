# database.py

from tinydb import TinyDB, Query

# ----------------------------------------------------------------------
# 1. Initialisation de la base de données
# ----------------------------------------------------------------------
# TinyDB stocke les données dans un fichier JSON.
# Ici, le fichier est situé dans : data/db.json
# S'il n'existe pas, TinyDB le crée automatiquement.
db = TinyDB("data/db.json")

# ----------------------------------------------------------------------
# 2. Déclaration des tables
# ----------------------------------------------------------------------
# Chaque table est l'équivalent d'une "collection" (comme en NoSQL).
# Cela permet de séparer proprement les joueurs et les tournois.
players_table = db.table("players")
tournaments_table = db.table("tournaments")

# ----------------------------------------------------------------------
# 3. Objets Query pour effectuer des recherches
# ----------------------------------------------------------------------
# Query() permet d'écrire des requêtes du type :
# players_table.get(PlayerQuery.national_id == "FR12345")
PlayerQuery = Query()
TournamentQuery = Query()
