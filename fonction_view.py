from PyQt6.QtWidgets import QPushButton, QListWidget, QLineEdit, QMessageBox, QDockWidget
from PyQt6.uic import loadUi
from sympy import SympifyError

from liste_fonctions_model import ListeFonctionsModel
import sympy as sp

class FonctionView(QDockWidget):
    saveButton : QPushButton
    addButton : QPushButton
    deleteButton : QPushButton

    listWidget : QListWidget

    lineEdit : QLineEdit

    def __init__(self, parent=None):
        super().__init__("Éditeur de fonctions", parent)
        loadUi('fonction_view.ui', self)

        self.liste_fonctions = ListeFonctionsModel("fonctions.json")
        self.display_fonctions()

        self.deleteButton.clicked.connect(lambda : self.remove_fonction())
        self.addButton.clicked.connect(lambda : self.add_fonction())
        self.saveButton.clicked.connect(lambda : self.save())

    def display_fonctions(self):
        self.listWidget.clear()
        for fonction in self.liste_fonctions.liste_fonctions:
            self.listWidget.addItem(fonction)

    def add_fonction(self):
        element_a_ajouter = self.lineEdit.text().strip()

        if not element_a_ajouter:
            return

        try:
            expr = sp.sympify(element_a_ajouter)

            x = sp.symbols('x')

            # Suggestion de l'IA : utiliser free_symbols.issubset({x}) pour attraper les variables qui ne sont pas x
            if not expr.free_symbols.issubset({x}):
                raise ValueError("La fonction doit contenir seulement la variable 'x'.")

            self.liste_fonctions.add_fonction(element_a_ajouter)
            self.display_fonctions()
            self.lineEdit.clear()

        # Suggestion de l'IA : utiliser un QMessageBox pour prévenir l'utilisateur
        except (SympifyError, ValueError):
            QMessageBox.warning(
                self,
                "Fonction invalide",
                "La fonction que vous tentez d'ajouter est invalide"
                "\nVérifiez la syntaxe"
            )


    def remove_fonction(self):
        element_selectionne = self.listWidget.currentItem().text()

        self.liste_fonctions.remove_fonction(element_selectionne)
        self.display_fonctions()

    def save(self):
        self.liste_fonctions.save_fonctions("fonctions.json")


