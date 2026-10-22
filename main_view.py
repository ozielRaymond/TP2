from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi("mainWindow.ui", self)
