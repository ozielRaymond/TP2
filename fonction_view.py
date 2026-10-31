from PyQt6.QtWidgets import QPushButton, QListWidget, QLineEdit, QMessageBox, QDockWidget
from PyQt6.uic import loadUi
from sympy import SympifyError
from liste_fonctions_model import ListeFonctionsModel
import sympy as sp


# L'IA a été consultée et utilisée dans cette classe
# pour contribuer à la documentation et
# me guider pour construire le processus de validation des fonctions.

class FonctionView(QDockWidget):
    """Fenêtre de type QDockWidget permettant d'ajouter, supprimer et sauvegarder des fonctions.

    Attributs :
        saveButton (QPushButton) : Bouton enregistrant les fonctions.
        addButton (QPushButton) : Bouton ajoutant la fonction saisie.
        deleteButton (QPushButton) : Bouton supprimant l'élément sélectionné.
        listWidget (QListWidget) : Widget affichant la liste des fonctions.
        lineEdit (QLineEdit) : Champ pour la saisie d'une nouvelle fonction.
        fonctions (ListeFonctionsModel) : Modèle assurant la persistance avec JSON.
    """

    saveButton: QPushButton
    addButton: QPushButton
    deleteButton: QPushButton

    listWidget: QListWidget

    lineEdit: QLineEdit

    def __init__(self, parent=None):
        """Initialise la vue : charge le composant UI et connecte les signaux.

        Args :
            parent (QWidget, optional): Le composant parent (MainView).
        """
        super().__init__(parent)
        loadUi('ui/fonction_view.ui', self)

        self.fonctions = ListeFonctionsModel("json_et_stylesheet/fonctions.json")

        self.display_fonctions()

        self.deleteButton.clicked.connect(lambda: self.remove_fonction())
        self.addButton.clicked.connect(lambda: self.add_fonction())
        self.saveButton.clicked.connect(lambda: self.save_modifications())
        self.lineEdit.textChanged.connect(lambda: self.lineEdit.setStyleSheet(""))

    def display_fonctions(self):
        """Met à jour l'affichage de la liste des fonctions."""
        self.listWidget.clear()
        for fonction in self.fonctions.liste_fonctions_str:
            self.listWidget.addItem(fonction)

    def save_modifications(self):
        """Sauvegarde la liste dans le fichier JSON, update MainView et ferme le dock."""
        self.fonctions.sauvegarder_fonctions("json_et_stylesheet/fonctions.json")

        # Aide de l'IA pour savoir comment désigner la fonction update_window du parent
        parent = self.parent()
        if parent and hasattr(parent, "update_window"):
            parent.update_window()

        self.close()

    def remove_fonction(self):
        """Supprime la fonction sélectionnée dans le QListWidget."""
        element_selectionne = self.listWidget.currentItem()
        if element_selectionne is None:
            return

        self.fonctions.remove_fonction(element_selectionne.text())
        self.display_fonctions()

    def add_fonction(self):
        """Valide et ajoute la fonction saisie par l'utilisateur.

        Vérifie avec SymPy que l'expression est correcte et ne dépend que de la variable 'x'.
        QMessageBox en cas d'erreur.
        """
        element_a_ajouter = self.lineEdit.text().strip()

        if not element_a_ajouter:
            self.lineEdit.setStyleSheet("""QLineEdit {background-color : #D9544D; }""")
            return

        try:
            expr = sp.sympify(element_a_ajouter)
            x = sp.symbols('x')

            # Suggestion de l'IA : utiliser free_symbols.issubset({x}) pour attraper les variables qui ne sont pas x
            if not expr.free_symbols.issubset({x}):
                raise ValueError("La fonction doit contenir seulement la variable 'x'.")

            self.fonctions.add_fonction(element_a_ajouter)
            self.display_fonctions()
            self.lineEdit.setStyleSheet("")
            self.lineEdit.clear()

        # Suggestion de l'IA : utiliser un QMessageBox pour prévenir l'utilisateur
        except (SympifyError, ValueError):
            self.lineEdit.setStyleSheet("""QLineEdit {background-color : #D9544D; }""")
            QMessageBox.warning(
                self,
                "Fonction invalide",
                "La fonction que vous tentez d'ajouter est invalide"
                "\nVérifiez la syntaxe"
            )
