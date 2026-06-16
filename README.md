# ♟️ Chess Tournament Manager  
Gestionnaire de tournois d’échecs — Projet Python (Architecture MVC)

---

## 🎯 Objectif du projet
Ce programme permet de gérer entièrement un tournoi d’échecs en utilisant un système Round‑Robin (tous les joueurs se rencontrent une fois).
Il offre une interface console moderne grâce à Rich, une structure claire grâce à l’architecture MVC, et une persistance des données via TinyDB.

Le gestionnaire permet :

- Création et gestion de tournois
- Ajout et gestion des joueurs
- Génération des rounds (Round‑Robin)
- Gestion des matchs et attribution des scores
- Historique des tournois
- Rapports détaillés
- Classement général
- Sauvegarde et chargement via TinyDB

---

## 🗂️ Structure du projet
```
CHESS_TOURNAMENT/
│
├── controllers/
│   ├── __init__.py
│   ├── menu_controller.py
│   ├── player_controller.py
│   ├── report_controller.py
│   ├── round_controller.py
│   └── tournament_controller.py
│
├── models/
│   ├── __init__.py
│   ├── match.py
│   ├── player.py
│   ├── round.py
│   └── tournament.py
│
├── views/
│   ├── __init__.py
│   ├── menu_view.py
│   ├── player_view.py
│   ├── report_view.py
│   ├── round_view.py
│   └── tournament_view.py
│
├── data/
│   └── db.json
│
├── flake8-report/        # Rapport HTML généré
│   └── index.html
├── database.py              
├── main.py               # Point d’entrée du programme
├── README.md
├── requirements.txt
└── .flake8
```

### ▶️ Exécution du programme

Assurez-vous d’avoir Python 3.10+ installé.

### 1. Installer les dépendances
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Lancer l’application
```
python main.py
```

### Générer le rapport :
```
flake8 --format=html --htmldir=flake8_rapport
```

### Le rapport sera disponible ici :
```
flake8-report/index.html
```

🧰 Technologies utilisées
```
Python 3

TinyDB — Base de données légère en JSON

Rich — Interface console améliorée

Flake8 + flake8-html — Analyse de qualité du code

Architecture MVC — Séparation claire des responsabilités
```



👤 Auteur
Kevin Delcroix  
2026
