from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QDoubleSpinBox
from PyQt6.uic import loadUi
from mpl_canvas import MPLCanvas
from fonctionmodel import FonctionModel
from fonction_view import FonctionView
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from liste_fonctions_model import ListeFonctionsModel


class MainView(QMainWindow):
    __model: FonctionModel

    comboBox: QComboBox

    widget: QWidget

    horizontalSlider: QSlider
    deriveeLabel: QLabel
    tangenceLabel: QLabel
    TVLabel: QLabel

    doubleSpinBox: QDoubleSpinBox
    doubleSpinBox_2: QDoubleSpinBox

    modifierFonctions: QAction

    def __init__(self):
        super().__init__()

        loadUi("mainWindow.ui", self)

        self.liste_fonctions = ListeFonctionsModel("fonctions.json")
        self.comboBox.addItems(self.liste_fonctions.liste_fonctions)

        self.doubleSpinBox.setValue(0)
        self.doubleSpinBox_2.setValue(10)

        self.model = FonctionModel(
            self.comboBox.currentText(),
            self.doubleSpinBox.value(),
            self.doubleSpinBox_2.value(),
            2
        )

        self.canvas = MPLCanvas(self.model)
        layout_f = QVBoxLayout(self.widget)
        layout_f.addWidget(self.canvas)

        self.horizontalSlider.setMinimum(int(self.model.minimum))
        self.horizontalSlider.setMaximum(int(self.model.maximum))
        self.horizontalSlider.setValue(self.model.tangente)

        self.deriveeLabel.setText("Fonction Dérivée : " + self.model.derivee_text())

        self.horizontalSlider.valueChanged.connect(self.update_valeurs_slide)
        self.comboBox.currentTextChanged.connect(self.charger_fonction)
        self.doubleSpinBox.valueChanged.connect(self.update_bounds)
        self.doubleSpinBox_2.valueChanged.connect(self.update_bounds)

        self.dock_widget = FonctionView(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_widget)
        self.modifierFonctions.triggered.connect(self.toggle_dock)

    def toggle_dock(self):
        if self.dock_widget.isVisible():
            self.dock_widget.setVisible(False)
        else:
            self.dock_widget.setVisible(True)


    def update_valeurs_slide(self, value):
        self.model.tangente = value
        self.tangenceLabel.setText("Point de tangence : " + str(value))
        self.TVLabel.setText("Taux de variation : " + str(self.model.differentie(value)))

    def update_bounds(self):
        value_min = self.doubleSpinBox.value()
        value_max = self.doubleSpinBox_2.value()

        if value_min < value_max:
            self.model.minimum = value_min
            self.model.maximum = value_max

            self.horizontalSlider.setMinimum(int(value_min))
            self.horizontalSlider.setMaximum(int(value_max))

            self.update_canvas()

    def update_canvas(self):
        if self.canvas:
            self.widget.layout().removeWidget(self.canvas)
            # Utilisation de l'IA pour bien comprendre la fonction deleteLater
            self.canvas.deleteLater()

        self.canvas = MPLCanvas(self.model)
        self.widget.layout().addWidget(self.canvas)

        self.deriveeLabel.setText("Fonction Dérivée : " + self.model.derivee_text())
        self.update_valeurs_slide(self.horizontalSlider.value())

    def update_window(self):
        self.comboBox.clear()
        self.liste_fonctions = ListeFonctionsModel("fonctions.json")
        self.comboBox.addItems(self.liste_fonctions.liste_fonctions)
        self.model.fonction = self.comboBox.currentText()
        self.update_canvas()

    def charger_fonction(self, texte_fonction):
        if texte_fonction:
            self.model.fonction = texte_fonction
            self.update_canvas()