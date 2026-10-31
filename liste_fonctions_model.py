import json


# L'IA a été consultée et utilisée dans cette classe
# pour contribuer à la documentation.

class ListeFonctionsModel:
    """Modèle gérant la liste des fonctions et la sérialisation de celles-ci.

    Attributs :
        liste_fonctions_str (list[str]) : Liste des fonctions enregistrées en string.
    """
    __liste_fonctions_str: list[str]

    def __init__(self, path_to_json: str):
        """Initialise le modèle et charge la liste depuis un fichier JSON.

        Args :
            path_to_json (str): Chemin d'accès au fichier JSON.
        """
        self.__liste_fonctions_str = []
        self.charger_fonctions(path_to_json)

    @property
    def liste_fonctions_str(self):
        """list[str] : Obtient la liste des fonctions."""
        return self.__liste_fonctions_str

    def charger_fonctions(self, path_to_json):
        """Charge les fonctions sauvegardées dans le fichier JSON.

        Args:
            path_to_json (str): Chemin d'accès vers le fichier JSON.
        """
        with open(path_to_json, "r", encoding="utf-8") as f:
            fonctions = json.load(f)
            for fonction in fonctions:
                self.__liste_fonctions_str.append(fonction)

    def sauvegarder_fonctions(self, path_to_json):
        """Écrit la liste de fonctions dans le fichier JSON.

        Args :
            path_to_json (str): Chemin vers le fichier JSON de destination.
        """
        with open(path_to_json, "w", encoding="utf-8") as f:
            json.dump(self.__liste_fonctions_str, f, indent=4)

    def add_fonction(self, fonction):
        """Ajoute une nouvelle fonction à la liste.

        Args
            fonction (str) : L'expression à ajouter.
        """
        self.__liste_fonctions_str.append(fonction)

    def remove_fonction(self, fonction):
        """Retire une fonction de la liste en mémoire.

        Args :
            fonction (str) : L'expression à supprimer.
        """
        self.__liste_fonctions_str.remove(fonction)
