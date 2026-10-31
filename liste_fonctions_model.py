import json


class ListeFonctionsModel:
    __liste_fonctions_str: list[str]

    def __init__(self, path_to_json: str):
        self.__liste_fonctions_str = []
        self.charger_fonctions(path_to_json)

    @property
    def liste_fonctions_str(self):
        return self.__liste_fonctions_str

    def charger_fonctions(self, path_to_json):
        with open(path_to_json, "r", encoding="utf-8") as f:
            fonctions = json.load(f)
            for fonction in fonctions:
                self.__liste_fonctions_str.append(fonction)

    def sauvegarder_fonctions(self, path_to_json):
        with open(path_to_json, "w", encoding="utf-8") as f:
            json.dump(self.__liste_fonctions_str, f, indent=4)

    def add_fonction(self, fonction):
        self.__liste_fonctions_str.append(fonction)

    def remove_fonction(self, fonction):
        self.__liste_fonctions_str.remove(fonction)
