from tinydb import TinyDB, Query

# Base de données principale
db = TinyDB("data/db.json")

# Tables
players_table = db.table("players")
tournaments_table = db.table("tournaments")

# Pour les recherches
PlayerQuery = Query()
TournamentQuery = Query()
