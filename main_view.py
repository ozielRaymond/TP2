from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.uic import loadUi
from mpl_canvas import MPLCanvas
from fonctionmodel import FonctionModel

class MainView(QMainWindow):
    __model : FonctionModel

    def __init__(self):
        super().__init__()

        #Test rapide de FonctionModel
        model = FonctionModel("3", 0, 10, 2)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        canvas = MPLCanvas(model)
        layout.addWidget(canvas)

        loadUi("mainWindow.ui", self)
