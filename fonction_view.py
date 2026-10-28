from PyQt6.QtWidgets import QDialog, QPushButton, QListWidget
from PyQt6.uic import loadUi
from liste_fonctions_model import ListeFonctionsModel

class FonctionView(QDialog):
    saveButton : QPushButton
    addButton : QPushButton
    deleteButton : QPushButton

    listWidget : QListWidget
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('fonction_view.ui', self)

        self.liste_fonctions = ListeFonctionsModel("fonctions.json")
        self.display_fonctions()

        self.deleteButton.clicked.connect(lambda : self.remove_fonction())

    def display_fonctions(self):
        for fonction in self.liste_fonctions.liste_fonctions:
            self.listWidget.addItem(fonction)

    def remove_fonction(self):
        element_selectionne = self.listWidget.currentItem().text()

        self.liste_fonctions.remove_fonction(element_selectionne)
        self.liste_fonctions.save_fonctions("fonctions.json")
        self.listWidget.takeItem(self.listWidget.currentRow())
