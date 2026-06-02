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
---
CHESS_TOURNAMENT/
│
├── controllers/
│   ├── player_controller.py
│   ├── round_controller.py
│   └── tournament_controller.py
│
├── models/
│   ├── player.py
│   ├── round.py
│   └── tournament.py
│
├── views/
│   ├── player_view.py
│   ├── round_view.py
│   └── tournament_view.py
│
├── data/
│   └── db.json
│
├── flake8-report/        # Rapport HTML généré (qualité du code)
├── main.py               # Point d’entrée du programme
├── requirements.txt
└── README.md
---

---

## ▶️ Exécution du programme

Assurez-vous d’avoir Python 3.10+ installé.

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
---
---
### 2. Lancer l’application
python main.py
---
### Générer le rapport :
```bash
flake8 --format=html --htmldir=flake8-report
---
### Le rapport sera disponible ici :
flake8-report/index.html

---
🧰 Technologies utilisées
Python 3

TinyDB — Base de données légère en JSON

Rich — Interface console améliorée

Flake8 + flake8-html — Analyse de qualité du code

Architecture MVC — Séparation claire des responsabilités

---
🧠 Points forts du projet
Architecture propre et modulaire

Gestion complète d’un tournoi Round‑Robin

Sauvegarde persistante des données

Interface console claire et ergonomique

Code entièrement validé par Flake8
---
👤 Auteur
Kevin Delcroix  
Projet OpenClassrooms — Développeur d’Applications Python
2026
