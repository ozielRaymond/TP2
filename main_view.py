from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QDoubleSpinBox, QFileDialog
from PyQt6.uic import loadUi
from fonction_view import FonctionView
from fonctionmodel import FonctionModel
from liste_fonctions_model import ListeFonctionsModel
from mpl_canvas import MPLCanvas


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
    exporterEnPDF : QAction
    toggleGrid : QAction
    couleurs : QAction

    bleuF : QAction
    vertF : QAction
    rougeF : QAction

    bleuD : QAction
    vertD : QAction
    rougeD : QAction

    bleuT : QAction
    vertT : QAction
    rougeT : QAction

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

        self.grid_enabeled = False
        self.colors = {"f": "blue", "f'": "blue", "t": "blue"}
        self.canvas = MPLCanvas(self.model, show_grid=self.grid_enabeled, colors=self.colors)
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
        self.exporterEnPDF.triggered.connect(self.export)
        self.toggleGrid.triggered.connect(self.toggle_grid)

        self.bleuF.triggered.connect(lambda: self.changer_couleur("f", "blue"))
        self.vertF.triggered.connect(lambda: self.changer_couleur("f", "green"))
        self.rougeF.triggered.connect(lambda: self.changer_couleur("f", "red"))

        self.bleuD.triggered.connect(lambda: self.changer_couleur("f'", "blue"))
        self.vertD.triggered.connect(lambda: self.changer_couleur("f'", "green"))
        self.rougeD.triggered.connect(lambda: self.changer_couleur("f'", "red"))

        self.bleuT.triggered.connect(lambda: self.changer_couleur("t", "blue"))
        self.vertT.triggered.connect(lambda: self.changer_couleur("t", "green"))
        self.rougeT.triggered.connect(lambda: self.changer_couleur("t", "red"))

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


        self.canvas = MPLCanvas(self.model, show_grid=self.grid_enabeled, colors=self.colors)
        self.widget.layout().addWidget(self.canvas)

        self.deriveeLabel.setText("Fonction Dérivée : " + self.model.derivee_text())
        self.update_valeurs_slide(self.horizontalSlider.value())

    def update_window(self):
        self.comboBox.clear()
        self.liste_fonctions = ListeFonctionsModel("fonctions.json")
        self.comboBox.addItems(self.liste_fonctions.liste_fonctions)
        self.model.fonction = self.comboBox.currentText()
        self.update_canvas()

    def toggle_grid(self, checked):
        self.grid_enabeled = checked
        self.update_canvas()

    def charger_fonction(self, texte_fonction):
        if texte_fonction:
            self.model.fonction = texte_fonction
            self.update_canvas()

    def changer_couleur(self, element, couleur):
        self.colors[element] = couleur
        self.update_canvas()

    # l'IA a été consulté pour construire la fonction
    def export(self):
        file_path = QFileDialog.getSaveFileName(self, "Exporter en PDF", "graphes.pdf", "Fichiers PDF (*.pdf)")
        if file_path:
            self.canvas.figure.savefig(file_path, format='pdf', bbox_inches='tight')