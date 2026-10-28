from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QSlider
from PyQt6.uic import loadUi
from mpl_canvas import MPLCanvas
from fonctionmodel import FonctionModel
from fonction_view import FonctionView
from PyQt6.QtGui import QAction

class MainView(QMainWindow):
    __model : FonctionModel

    fonctionLineEdit: QLineEdit

    widget : QWidget

    horizontalSlider : QSlider
    deriveeLabel : QLabel
    tangenceLabel : QLabel
    TVLabel : QLabel

    modifierFonctions : QAction

    def __init__(self):
        super().__init__()

        loadUi("mainWindow.ui", self)

        self.modifierFonctions.triggered.connect(self.ouvrir_q_dialog)

        #Test rapide de FonctionModel
        self.__model = FonctionModel("10*x^2", 0, 10, 2)
        self.canvas = MPLCanvas(self.__model)

        layout_f = QVBoxLayout(self.widget)
        layout_f.addWidget(self.canvas)

        self.horizontalSlider.setMinimum(self.__model.minimum)
        self.horizontalSlider.setMaximum(self.__model.maximum)

        self.deriveeLabel.setText("Fonction Dérivée : " + self.__model.derivee_text())
        self.horizontalSlider.valueChanged.connect(self.update_valeurs_slide)

    def update_valeurs_slide(self, value):
        self.tangenceLabel.setText("Point de tangence : " + str(value))
        self.TVLabel.setText("Taux de variation : " + str(self.__model.differentie(value)))

    def ouvrir_q_dialog(self):
        dialog = FonctionView(self)
        dialog.exec()