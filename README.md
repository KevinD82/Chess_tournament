# ♟️ Chess Tournament Manager  
Gestionnaire de tournois d’échecs — Projet Python (Architecture MVC)

---

## 🎯 Objectif du projet
Ce programme permet de gérer entièrement un tournoi d’échecs :
- Création de tournois
- Ajout et gestion des joueurs
- Gestion des rounds et des matchs
- Attribution des scores
- Classement final
- Sauvegarde et chargement via TinyDB

Le projet suit une architecture **MVC (Model – View – Controller)** pour garantir une structure claire, maintenable et évolutive.

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
└── requirements.txt
```

### ▶️ Exécution du programme

Assurez-vous d’avoir Python 3.10+ installé.

### 1. Installer les dépendances
```
pip install -r requirements.txt
```

### 2. Lancer l’application
```
python main.py
```

### Générer le rapport :
```
flake8 --format=html --htmldir=flake8-report
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
