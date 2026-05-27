# main.py

# Le MenuController est le point d'entrée principal de l'application.
# Il gère la navigation entre toutes les fonctionnalités :
# - gestion des joueurs
# - gestion des tournois
# - rapports
from controllers.menu_controller import MenuController


def main():
    """
    Fonction principale de l'application.
    Elle instancie le contrôleur du menu et lance la boucle principale.
    """
    app = MenuController()
    app.run()  # Démarre l'application (boucle infinie jusqu'à "Quitter")


# Ce bloc garantit que main() n'est exécuté que si le fichier est lancé directement.
# Il ne s'exécute pas si le fichier est importé ailleurs.
if __name__ == "__main__":
    main()
