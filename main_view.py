from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QDoubleSpinBox, QFileDialog, \
    QLineEdit
from PyQt6.uic import loadUi
import io
import matplotlib.pyplot as plt

from fonction_view import FonctionView
from fonction_model import FonctionModel
from liste_fonctions_model import ListeFonctionsModel
from mpl_canvas import MPLCanvas


# L'IA a été consultée et utilisée dans cette classe
# pour contribuer à la documentation et
# me guider dans l'implémentation du mécanisme d'affichage du LaTex avec pixmap
# et de l'export en format PDF.

class MainView(QMainWindow):
    """Fenêtre principale gérant l'ensemble de la vue de l'application.

    Attributs :
        widget (QWidget) : Widget du canvas graphique.
        comboBox (QComboBox) : Sélecteur de fonctions.
        horizontalSlider (QSlider) : Slider d'ajustement du point de tangente.
        lineEditTV (QLineEdit) : Champ d'affichage du taux de variation.
        lineEditTangente (QLineEdit) : Champ d'affichage de la tangente.
        deriveeLabel (QLabel) : Label d'affichage de la dérivée en LaTeX.
        minSpinBox (QDoubleSpinBox) : Contrôle du minimum de la fonction en x.
        maxSpinBox (QDoubleSpinBox) : Contrôle du maximum de la fonction en x.
        model (FonctionModel) : Modèle de la fonction.
        canvas (MPLCanvas) : Composant de rendu Matplotlib.
        dock_widget (FonctionView) : QDockWidget pour l'édition de la liste.
    """

    widget: QWidget
    comboBox: QComboBox
    horizontalSlider: QSlider
    lineEditTV: QLineEdit
    lineEditTangente: QLineEdit
    deriveeLabel: QLabel
    minSpinBox: QDoubleSpinBox
    maxSpinBox: QDoubleSpinBox

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
        """Initialise l'interface principale et connecte tous les événements."""
        super().__init__()

        loadUi("ui/main_view.ui", self)

        with open("json_et_stylesheet/style.css", "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.lineEditTV.setReadOnly(True)
        self.lineEditTangente.setReadOnly(True)

        self.liste_fonctions = ListeFonctionsModel("json_et_stylesheet/fonctions.json")
        self.comboBox.addItems(self.liste_fonctions.liste_fonctions_str)

        self.minSpinBox.setValue(0)
        self.maxSpinBox.setValue(10)

        self.model = FonctionModel(
            self.comboBox.currentText(),
            self.minSpinBox.value(),
            self.maxSpinBox.value(),
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
        self.minSpinBox.valueChanged.connect(self.update_bounds)
        self.maxSpinBox.valueChanged.connect(self.update_bounds)

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
        """Affiche le DockWidget selon son dernier état d'affichage."""
        self.dock_widget.setVisible(True)
        if self.was_docked:
            self.dock_widget.setFloating(False)
        else:
            self.dock_widget.setFloating(True)

    def action_masquer(self):
        """Masque le DockWidget"""
        self.was_docked = not self.dock_widget.isFloating()
        self.dock_widget.setVisible(False)

    def action_docker(self):
        """Ancre le DockWidget sur le côté droit de la fenêtre."""
        self.was_docked = True
        self.dock_widget.setVisible(True)
        self.dock_widget.setFloating(False)

    def action_detacher(self):
        """Détache le DockWidget sous forme de floating window."""
        self.was_docked = False
        self.dock_widget.setVisible(True)
        self.dock_widget.setFloating(True)

    def update_valeurs_slide(self, value):
        """Met à jour les champs textuels lors du déplacement du slider de la tangente.

        Args :
            value (int) : Nouvelle valeur de la tangente issue du slider.
        """
        self.model.tangente = value
        y = self.model.get_y_tangente(value)
        taux_de_variation = self.model.get_taux_variation(value)
        self.lineEditTangente.setText(f"({value:.2f}, {y:.2f})")
        self.lineEditTV.setText(f"{taux_de_variation:.2f}")

    def update_bounds(self):
        """Valide et applique les bornes de la fonction spécifiées dans les QDoubleSpinBox."""
        value_min = self.minSpinBox.value()
        value_max = self.maxSpinBox.value()

        if value_min < value_max:
            self.model.minimum = value_min
            self.model.maximum = value_max
            self.horizontalSlider.setMinimum(int(value_min))
            self.horizontalSlider.setMaximum(int(value_max))
            self.update_canvas()

    def update_latex_label(self):
        """Génère le rendu LaTeX de la dérivée et met à jour la pixmap dans deriveeLabel."""
        latex_derivee = self.model.derivee_latex()
        pixmap = self.render_latex_to_pixmap(latex_derivee)
        self.deriveeLabel.setPixmap(pixmap)

    def update_canvas(self):
        """Enlève l'ancien canvas et en réinstancie un nouveau pour rafraîchir l'affichage."""
        if self.canvas:
            self.widget.layout().removeWidget(self.canvas)
            self.canvas.deleteLater()

        self.canvas = MPLCanvas(self.model, show_grid=self.grid_enabeled, colors=self.colors)
        self.widget.layout().addWidget(self.canvas)
        self.update_latex_label()
        self.update_valeurs_slide(self.horizontalSlider.value())

    def update_window(self):
        """Actualise la liste des fonctions à partir du fichier JSON et actualise l'affichage."""
        self.comboBox.clear()
        self.liste_fonctions = ListeFonctionsModel("json_et_stylesheet/fonctions.json")
        self.comboBox.addItems(self.liste_fonctions.liste_fonctions_str)
        self.model.fonction = self.comboBox.currentText()
        self.update_canvas()

    def toggle_grid(self, checked):
        """Active ou désactive la grille sur les sous-graphiques.

        Args :
            checked (bool) : État de la sélection de la grille dans le menu.
        """
        self.grid_enabeled = checked
        self.update_canvas()

    def charger_fonction(self, texte_fonction):
        """Change la fonction sélectionnée dans le modèle et dessine les graphiques.

        Args :
            texte_fonction (str) : L'expression de la fonction sélectionnée.
        """
        if texte_fonction:
            self.model.fonction = texte_fonction
            self.update_canvas()

    def changer_couleur(self, element, couleur):
        """Met à jour la couleur d'une courbe spécifique.

        Args:
            element (str): L'identifiant de la courbe ('f', "f'", 't').
            couleur (str): Le nom de la couleur ('blue', 'green', 'red').
        """
        self.colors[element] = couleur
        self.update_canvas()

    # L'IA a été consultée pour construire la fonction et comprendre le mécanisme d'export.
    def export_pdf(self):
        """Ouvre une boîte de dialogue pour enregistrer les graphiques Matplotlib en format PDF."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Exporter en PDF", "graphes.pdf", "Fichiers PDF (*.pdf)")
        if file_path:
            self.canvas.figure.savefig(file_path, format='pdf', bbox_inches='tight')

    # L'IA a été consultée pour construire et comprendre la méthode de transformation en pixmap.
    @staticmethod
    def render_latex_to_pixmap(latex_str):
        """Convertit une chaîne LaTeX en image QPixmap via une figure Matplotlib.

        Args :
            latex_str (str) : L'expression LaTeX

            Returns :
                QPixmap : L'image générée sous forme d'objet QPixmap transparent.
        """

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
