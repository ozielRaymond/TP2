from PyQt6.QtWidgets import QDialog, QPushButton, QListWidget, QLineEdit
from PyQt6.uic import loadUi
from liste_fonctions_model import ListeFonctionsModel

class FonctionView(QDialog):
    saveButton : QPushButton
    addButton : QPushButton
    deleteButton : QPushButton

    listWidget : QListWidget

    lineEdit : QLineEdit

    def __init__(self, parent=None):
        super().__init__(parent)
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
        element_a_ajouter = self.lineEdit.text()

        self.liste_fonctions.add_fonction(element_a_ajouter)
        self.display_fonctions()
        self.lineEdit.clear()

    def remove_fonction(self):
        element_selectionne = self.listWidget.currentItem().text()

        self.liste_fonctions.remove_fonction(element_selectionne)
        self.display_fonctions()

    def save(self):
        self.liste_fonctions.save_fonctions("fonctions.json")
        self.accept()


