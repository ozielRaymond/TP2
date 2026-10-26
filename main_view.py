from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit
from PyQt6.uic import loadUi
from mpl_canvas import MPLCanvas
from fonctionmodel import FonctionModel

class MainView(QMainWindow):
    __model : FonctionModel
    widget : QWidget

    lineEdit : QLineEdit

    def __init__(self):
        super().__init__()

        loadUi("mainWindow.ui", self)

        #Test rapide de FonctionModel
        self.__model = FonctionModel("10*x", 0, 10, 2)
        self.canvas = MPLCanvas(self.__model, False)


        layout_f = QVBoxLayout(self.widget)
        layout_f.addWidget(self.canvas)




