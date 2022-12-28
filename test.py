import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))
        self.tray_icon.setVisible(True)

        # Create a menu for the system tray icon
        tray_menu = QMenu()
        restore_action = QAction("Restore", self)
        quit_action = QAction("Quit", self)
        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)

        # Add the menu to the system tray icon
        self.tray_icon.setContextMenu(tray_menu)

        # Connect the restore action to the restore slot
        restore_action.triggered.connect(self.show)

        # Connect the quit action to the quit slot
        quit_action.triggered.connect(self.close)

    def closeEvent(self, event):
        # Hide the main window and send it to the system tray
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Application minimized to tray",
                                   "The application has been minimized to the system tray. Click the tray icon to restore the application.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())