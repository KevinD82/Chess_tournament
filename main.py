# main.py
"""
Point d'entrée principal de l'application.

Ce fichier ne contient volontairement aucune logique métier.
Il instancie simplement le contrôleur principal (MenuController)
et lance la boucle de navigation de l'application.

Architecture MVC :
- Modèles  : données (joueurs, tournois, rounds…)
- Vues     : affichage et saisie utilisateur
- Contrôleurs : logique métier et navigation

Ici, main.py sert uniquement à démarrer l'application.
"""

from controllers.menu_controller import MenuController


def main():
    """Instancie le contrôleur principal et lance l'application."""
    app = MenuController()
    app.run()


if __name__ == "__main__":
    main()
