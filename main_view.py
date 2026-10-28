from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QSlider, QComboBox
from PyQt6.uic import loadUi
from mpl_canvas import MPLCanvas
from fonctionmodel import FonctionModel
from fonction_view import FonctionView
from PyQt6.QtGui import QAction
from liste_fonctions_model import ListeFonctionsModel


class MainView(QMainWindow):
    __model: FonctionModel

    comboBox: QComboBox

    widget: QWidget

    horizontalSlider: QSlider
    deriveeLabel: QLabel
    tangenceLabel: QLabel
    TVLabel: QLabel

    modifierFonctions: QAction

    def __init__(self):
        super().__init__()

        loadUi("mainWindow.ui", self)

        self.modifierFonctions.triggered.connect(self.ouvrir_q_dialog)

        self.liste_fonctions = ListeFonctionsModel("fonctions.json")
        self.comboBox.addItems(self.liste_fonctions.liste_fonctions)

        self.model = FonctionModel(self.comboBox.currentText(), 0, 10, 2)

        self.canvas = MPLCanvas(self.model)
        layout_f = QVBoxLayout(self.widget)
        layout_f.addWidget(self.canvas)

        self.horizontalSlider.setMinimum(self.model.minimum)
        self.horizontalSlider.setMaximum(self.model.maximum)

        self.deriveeLabel.setText("Fonction Dérivée : " + self.model.derivee_text())

        self.horizontalSlider.valueChanged.connect(self.update_valeurs_slide)
        self.comboBox.currentTextChanged.connect(self.charger_fonction)

    def update_valeurs_slide(self, value):
        self.tangenceLabel.setText("Point de tangence : " + str(value))
        self.TVLabel.setText("Taux de variation : " + str(self.model.differentie(value)))

    def ouvrir_q_dialog(self):
        dialog = FonctionView(self)
        dialog.exec()
        self.update_window()

    def update_window(self):
        self.comboBox.clear()

        self.liste_fonctions = ListeFonctionsModel("fonctions.json")
        self.comboBox.addItems(self.liste_fonctions.liste_fonctions)

        self.model = FonctionModel(self.comboBox.currentText(), 0, 10, 2)

        if self.canvas:
            self.widget.layout().removeWidget(self.canvas)
            # Utilisation de l'IA pour bien comprendre la fonction deleteLater
            self.canvas.deleteLater()

        self.canvas = MPLCanvas(self.model)
        self.widget.layout().addWidget(self.canvas)

        self.horizontalSlider.setMinimum(self.model.minimum)
        self.horizontalSlider.setMaximum(self.model.maximum)

        self.deriveeLabel.setText("Fonction Dérivée : " + self.model.derivee_text())

    def charger_fonction(self, texte_fonction):
        if texte_fonction:
            self.model.fonction = texte_fonction

            if self.canvas:
                self.widget.layout().removeWidget(self.canvas)
                # Utilisation de l'IA pour bien comprendre la fonction deleteLater
                self.canvas.deleteLater()

            self.canvas = MPLCanvas(self.model)
            self.widget.layout().addWidget(self.canvas)

            self.deriveeLabel.setText("Fonction Dérivée : " + self.model.derivee_text())
            self.update_valeurs_slide(self.horizontalSlider.value())
