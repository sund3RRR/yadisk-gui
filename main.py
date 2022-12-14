import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class App(QMainWindow):
    def __init__(self) -> None:
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":    
    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec())