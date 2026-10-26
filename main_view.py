from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.uic import loadUi
from mpl_canvas import MPLCanvas
from fonctionmodel import FonctionModel

class MainView(QMainWindow):
    __model : FonctionModel
    widget : QWidget

    def __init__(self):
        super().__init__()

        loadUi("mainWindow.ui", self)

        #Test rapide de FonctionModel
        self.__model = FonctionModel("3*x+1", 0, 10, 2)

        self.canvas = MPLCanvas(self.__model)

        layout = QVBoxLayout(self.widget)
        layout.addWidget(self.canvas)


