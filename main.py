import sys

from PyQt6.QtWidgets import QApplication

from main_view import MainView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MainView()
    fenetre.show()
    sys.exit(app.exec())