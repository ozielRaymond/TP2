from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QDoubleSpinBox, QFileDialog, \
    QLineEdit
from PyQt6.uic import loadUi
import io
import matplotlib.pyplot as plt

from fonction_view import FonctionView
from fonctionmodel import FonctionModel
from liste_fonctions_model import ListeFonctionsModel
from mpl_canvas import MPLCanvas


class MainView(QMainWindow):
    __model: FonctionModel

    widget: QWidget

    comboBox: QComboBox
    horizontalSlider: QSlider
    deriveeLabel: QLabel
    tangenceLabel: QLabel
    TVLabel: QLabel
    lineEditTV: QLineEdit
    lineEditTangente: QLineEdit
    label: QLabel

    doubleSpinBox: QDoubleSpinBox
    doubleSpinBox_2: QDoubleSpinBox

    modifierFonctions: QAction
    exporterEnPDF: QAction
    toggleGrid: QAction

    bleuF: QAction
    vertF: QAction
    rougeF: QAction
    bleuD: QAction
    vertD: QAction
    rougeD: QAction
    bleuT: QAction
    vertT: QAction
    rougeT: QAction

    actionOuvrir: QAction
    actionMasquer: QAction
    actionDocker: QAction
    actionD_tacher: QAction

    def __init__(self):
        super().__init__()

        loadUi("mainWindow.ui", self)

        with open("style.css", "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.lineEditTV.setReadOnly(True)
        self.lineEditTangente.setReadOnly(True)

        self.liste_fonctions = ListeFonctionsModel("fonctions.json")
        self.comboBox.addItems(self.liste_fonctions.liste_fonctions_str)

        self.doubleSpinBox.setValue(0)
        self.doubleSpinBox_2.setValue(10)

        self.model = FonctionModel(
            self.comboBox.currentText(),
            self.doubleSpinBox.value(),
            self.doubleSpinBox_2.value(),
            2
        )

        self.grid_enabeled = False
        self.colors = {"f": "blue", "f'": "blue", "t": "red"}
        self.canvas = MPLCanvas(self.model, show_grid=self.grid_enabeled, colors=self.colors)
        layout_f = QVBoxLayout(self.widget)
        layout_f.addWidget(self.canvas)

        self.horizontalSlider.setMinimum(int(self.model.minimum))
        self.horizontalSlider.setMaximum(int(self.model.maximum))
        self.horizontalSlider.setValue(int(self.model.tangente))

        self.update_latex_label()

        self.horizontalSlider.valueChanged.connect(self.update_valeurs_slide)
        self.horizontalSlider.sliderReleased.connect(self.update_canvas)
        self.comboBox.currentTextChanged.connect(self.charger_fonction)
        self.doubleSpinBox.valueChanged.connect(self.update_bounds)
        self.doubleSpinBox_2.valueChanged.connect(self.update_bounds)

        self.dock_widget = FonctionView(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_widget)
        self.dock_widget.setFloating(True)
        self.was_docked = False
        self.dock_widget.setVisible(False)

        self.actionOuvrir.triggered.connect(self.action_ouvrir)
        self.actionMasquer.triggered.connect(self.action_masquer)
        self.actionDocker.triggered.connect(self.action_docker)
        self.actionD_tacher.triggered.connect(self.action_detacher)
        self.exporterEnPDF.triggered.connect(self.export_pdf)
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

    def action_ouvrir(self):
        self.dock_widget.setVisible(True)
        if self.was_docked:
            self.dock_widget.setFloating(False)
        else:
            self.dock_widget.setFloating(True)

    def action_masquer(self):
        self.was_docked = not self.dock_widget.isFloating()
        self.dock_widget.setVisible(False)

    def action_docker(self):
        self.was_docked = True
        self.dock_widget.setVisible(True)
        self.dock_widget.setFloating(False)

    def action_detacher(self):
        self.was_docked = False
        self.dock_widget.setVisible(True)
        self.dock_widget.setFloating(True)

    def update_valeurs_slide(self, value):
        self.model.tangente = value
        y = self.model.get_y_tangente(value)
        taux_de_variation = self.model.get_taux_variation(value)
        self.lineEditTangente.setText(f"({value:.2f}, {y:.2f})")
        self.lineEditTV.setText(f"{taux_de_variation:.2f}")

    def update_bounds(self):
        value_min = self.doubleSpinBox.value()
        value_max = self.doubleSpinBox_2.value()

        if value_min < value_max:
            self.model.minimum = value_min
            self.model.maximum = value_max
            self.horizontalSlider.setMinimum(int(value_min))
            self.horizontalSlider.setMaximum(int(value_max))
            self.update_canvas()

    # Change la pixmap pour la nouvelle pixmap
    def update_latex_label(self):
        latex_derivee = self.model.derivee_latex()
        pixmap = self.render_latex_to_pixmap(latex_derivee)
        self.label.setPixmap(pixmap)

    def update_canvas(self):
        if self.canvas:
            self.widget.layout().removeWidget(self.canvas)
            self.canvas.deleteLater()

        self.canvas = MPLCanvas(self.model, show_grid=self.grid_enabeled, colors=self.colors)
        self.widget.layout().addWidget(self.canvas)
        self.update_latex_label()
        self.update_valeurs_slide(self.horizontalSlider.value())

    def update_window(self):
        self.comboBox.clear()
        self.liste_fonctions = ListeFonctionsModel("fonctions.json")
        self.comboBox.addItems(self.liste_fonctions.liste_fonctions_str)
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
    def export_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Exporter en PDF", "graphes.pdf", "Fichiers PDF (*.pdf)")
        if file_path:
            self.canvas.figure.savefig(file_path, format='pdf', bbox_inches='tight')

    @staticmethod
    def render_latex_to_pixmap(latex_str):
        # La méthode crée un pixmap (Une image de l'expression en latex avec matplotlib).
        fig = plt.figure(figsize=(0.01, 0.01), dpi=150)

        # Ajoute $ pour activer le mode math de matplotlib
        fig.text(0, 0, f"${latex_str}$", fontsize=8, color="white")

        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', transparent=True, dpi=150)
        plt.close(fig)

        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())
        return pixmap
