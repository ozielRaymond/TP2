from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

class FonctionView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('fonction_view.ui', self)