import json


class ListeFonctionsModel:
    liste_fonctions_str: list[str]

    def __init__(self, path_to_json: str):
        self.liste_fonctions_str = []
        self.charger_fonctions(path_to_json)

    def charger_fonctions(self, path_to_json):
        with open(path_to_json, "r", encoding="utf-8") as f:
            fonctions = json.load(f)
            for fonction in fonctions:
                self.liste_fonctions_str.append(fonction)

    def sauvegarder_fonctions(self, path_to_json):
        with open(path_to_json, "w", encoding="utf-8") as f:
            json.dump(self.liste_fonctions_str, f, indent=4)

    def add_fonction(self, fonction):
        self.liste_fonctions_str.append(fonction)

    def remove_fonction(self, fonction):
        self.liste_fonctions_str.remove(fonction)
