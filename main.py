import sys, subprocess
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from form.welcome_from import Ui_MainWindow as WelcomeForm
from form.install_form import Ui_MainWindow as InstallForm
from form.setup_1_form import Ui_MainWindow as SetupForm_1
from form.setup_2_form import Ui_MainWindow as SetupForm_2


class SettingWindow(QStackedWidget):
    def __init__(self):
        super(SettingWindow, self).__init__()

        self.welcomeWindow = WelcomeWindow(self)
        self.installWindow = InstallWindow(self)
        self.setupWindow_1 = SetupWindow_1(self)
        self.setupWindow_2 = SetupWindow_2(self)

        self.addWidget(self.welcomeWindow)
        self.addWidget(self.installWindow)
        self.addWidget(self.setupWindow_1)
        self.addWidget(self.setupWindow_2)

        self.trayIcon = SystemTrayIcon(QIcon("src/yandex_disk_icon.svg"), self)
        self.setWindowTitle("Яндекс.Диск")
        self.trayIcon.setVisible(True)
        app_icon = QIcon("src/yandex_disk_icon_transparent.png")

        app.setWindowIcon(app_icon)

    def close_app(self):
        app.exit()


    def closeEvent(self, event):
        # Hide the main window and send it to the system tray
        event.ignore()
        self.hide()
        self.trayIcon.showMessage("Яндекс.Диск работает!",
                                    "Приложение было свёрнуто в системный трей.", msecs=3000)
            


class WelcomeWindow(QMainWindow):
    def __init__(self, mainWindow :QStackedWidget) -> None:
        super(WelcomeWindow, self).__init__()
        self.ui = WelcomeForm()
        self.ui.setupUi(self)
        self.mainWindow = mainWindow
        self.ui.further_button.clicked.connect(self.next_stage)

        self.need_to_install_yadisk = self.is_yadisk_installed()
    
    def next_stage(self):
        if self.need_to_install_yadisk:
            self.mainWindow.setCurrentIndex(self.mainWindow.currentIndex() + 1)
        else:
            self.mainWindow.setCurrentIndex(self.mainWindow.currentIndex() + 2)

    def is_yadisk_installed(self):
        yadisk_version = str(subprocess.Popen("yandex-disk -v", shell=True, stdout=subprocess.PIPE).stdout.read())
        if "command not found" in yadisk_version:
            return False
        else:
            return True


class InstallWindow(QMainWindow):
    def __init__(self, mainWindow :QStackedWidget) -> None:
        super(InstallWindow, self).__init__()
        self.ui = InstallForm()
        self.ui.setupUi(self)
        self.mainWindow = mainWindow

        self.ui.further_button.clicked.connect(self.next_stage)
        self.ui.install_button.clicked.connect(self.install_yadisk)
    
    def next_stage(self):
        self.mainWindow.setCurrentIndex(self.mainWindow.currentIndex() + 1)

    def install_yadisk(self):
        pass



class SetupWindow_1(QMainWindow):
    def __init__(self, mainWindow :QStackedWidget) -> None:
        super(SetupWindow_1, self).__init__()
        self.ui = SetupForm_1()
        self.ui.setupUi(self)
        self.mainWindow = mainWindow

        self.ui.further_button.clicked.connect(self.next_stage)
    
    def next_stage(self):
        self.mainWindow.setCurrentIndex(self.mainWindow.currentIndex() + 1)


class SetupWindow_2(QMainWindow):
    def __init__(self, mainWindow :QStackedWidget) -> None:
        super(SetupWindow_2, self).__init__()
        self.ui = SetupForm_2()
        self.ui.setupUi(self)
        self.mainWindow = mainWindow

        self.ui.finish_button.clicked.connect(self.finish)
    
    def finish(self):
        self.mainWindow.close()


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.mainWindow = parent

        menu = QMenu(parent)
        self.setContextMenu(menu)

        self.activated.connect(self.tray_icon_activated)

        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.mainWindow.close_app)
        
        
    def tray_icon_activated(self):
        if self.mainWindow.isVisible():
            self.mainWindow.hide()
        else:
            self.mainWindow.show()



if __name__ == "__main__":    
    app = QApplication(sys.argv)
    mainWindow = SettingWindow()
    mainWindow.show()
    sys.exit(app.exec())