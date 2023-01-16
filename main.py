import sys, subprocess, asyncio, pyperclip, time
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from form.welcome_from import Ui_MainWindow as WelcomeForm
from form.install_form import Ui_MainWindow as InstallForm
from form.setup_1_form import Ui_MainWindow as SetupForm_1
from form.setup_2_form import Ui_MainWindow as SetupForm_2

def is_yadisk_installed():
    try:
        subprocess.run(["yandex-disk"])         
        return True
    except:
        return False

class YandexDiskThread(QObject):
    finished = pyqtSignal()
    def __init__(self, status_label):
        QThread.__init__(self)
     
        self.status_label = status_label

    def run_yandex_disk(self) -> None:
        self.yd_process = subprocess.Popen(
            ["yandex-disk", "token"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        self.status_label.setText("Обрабатывается...")
        while self.yd_process.poll() == None:
            time.sleep(1)
        self.status_label.setText("Готово")
        self.finished.emit()

    def get_code(self):
        while True:
            try:
                print(self.yd_process)
                output = self.yd_process.stdout.read(150).decode("UTF-8")       
                words = output.split(" ")
                for word in words:
                    if "‘" == word[0] and "’" == word[-1]:
                        code = word[1:-1]
                
                return code
            except:
                time.sleep(0.1)
        


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
        self.need_to_install_yadisk = not is_yadisk_installed()
    
    def next_stage(self):
        if self.need_to_install_yadisk:
            self.mainWindow.setCurrentIndex(self.mainWindow.currentIndex() + 1)
        else:
            self.mainWindow.setCurrentIndex(self.mainWindow.currentIndex() + 2)


class InstallWindow(QMainWindow):
    def __init__(self, mainWindow :QStackedWidget) -> None:
        super(InstallWindow, self).__init__()
        self.ui = InstallForm()
        self.ui.setupUi(self)
        self.mainWindow = mainWindow

        self.ui.further_button.setDisabled(True)
        self.ui.further_button.clicked.connect(self.next_stage)
        self.ui.install_button.clicked.connect(self.install_yadisk)
    
    def next_stage(self):
        self.mainWindow.setCurrentIndex(self.mainWindow.currentIndex() + 1)

    def install_yadisk(self):
        subprocess.run(["bash", "scripts/install_yd.sh"]).stdout

        is_installation_success = is_yadisk_installed()
        if is_installation_success:
            self.ui.install_status_label.setText("Установка прошла успешно!")
            self.ui.further_button.setEnabled(True)
        else:
            self.ui.install_status_label.setText("Возникла ошибка")
        
        self.ui.install_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)



class SetupWindow_1(QMainWindow):
    def __init__(self, mainWindow :QStackedWidget) -> None:
        super(SetupWindow_1, self).__init__()
        self.ui = SetupForm_1()
        self.ui.setupUi(self)
        self.mainWindow = mainWindow
        
        self.yd_link = "https://ya.ru/device"
        
        #self.ui.further_button.setDisabled(True)

        self.ui.auth_button.clicked.connect(self.authorize)
        self.ui.get_code_button.clicked.connect(self.get_code)
        self.ui.copy_button.clicked.connect(lambda: pyperclip.copy(self.ui.code_output.text()))
        self.ui.grant_access_button.clicked.connect(self.grant_access)
        self.ui.further_button.clicked.connect(self.next_stage)

    def get_code(self):
        self.thread = QThread(self)
        self.yd_worker = YandexDiskThread(self.ui.auth_status)
        self.yd_worker.moveToThread(self.thread)

        self.thread.started.connect(self.yd_worker.run_yandex_disk)
        self.yd_worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(lambda: self.ui.further_button.setEnabled(True))
        self.thread.start()

        self.ui.code_output.setText(self.yd_worker.get_code())


    def grant_access(self):
        subprocess.run(["xdg-open", self.yd_link])


    def authorize(self):
        subprocess.run(["xdg-open", "https://passport.yandex.ru/auth/welcome"])
 

    def next_stage(self):
        self.mainWindow.setCurrentIndex(self.mainWindow.currentIndex() + 1)


class SetupWindow_2(QMainWindow):
    def __init__(self, mainWindow :QStackedWidget) -> None:
        super(SetupWindow_2, self).__init__()
        self.ui = SetupForm_2()
        self.ui.setupUi(self)
        self.mainWindow = mainWindow

        self.ui.dir_select_button.clicked.connect(self.select_dir)
        self.ui.add_folder_button.clicked.connect(self.add_folder_input)
        self.ui.remove_folder_button.clicked.connect(self.remove_folder_input)
        self.ui.finish_button.clicked.connect(self.finish)
    
    def select_dir(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, 'Выберите папку')
        self.ui.dir_label.setText(self.dir_path)
    
    def add_folder_input(self):
        new_folder_item = QLabel()
        new_folder_item.setPixmap(self.ui.folder_icon.pixmap())
        new_folder_item.setScaledContents(True)
        new_folder_item.setMinimumSize(30, 30)
        new_folder_item.setMaximumSize(30, 30)

        new_folder_input = QLineEdit(self.ui.folder_input) 
        row = self.ui.add_folder_layout.count() // 2
        self.ui.add_folder_layout.addWidget(new_folder_item, row, 0)
        self.ui.add_folder_layout.addWidget(new_folder_input, row, 1)

        self.ui.frame.setMinimumHeight(self.ui.frame.maximumHeight() + 30)
        self.ui.frame.setMaximumHeight(self.ui.frame.maximumHeight() + 30)
        self.mainWindow.resize(self.mainWindow.width(), self.mainWindow.height() + 30)


    def remove_folder_input(self):
        row = self.ui.add_folder_layout.count() // 2
        if row > 0:
            remove_icon = self.ui.add_folder_layout.itemAtPosition(row-1, 0)
            remove_input = self.ui.add_folder_layout.itemAtPosition(row-1, 1)
            remove_icon.widget().setParent(None)
            remove_input.widget().setParent(None)
            self.ui.frame.setMinimumHeight(self.ui.frame.maximumHeight() - 30)
            self.ui.frame.setMaximumHeight(self.ui.frame.maximumHeight() - 30)
            self.mainWindow.resize(self.mainWindow.width(), self.mainWindow.height() - 30)
 

    def finish(self):
        yd_directory = self.ui.dir_label.text()
        yd_exclude_dirs = []

        row_count = self.ui.add_folder_layout.count() // 2
        for i in range(0, row_count):
            yd_exclude_dirs.append(self.ui.add_folder_layout.itemAtPosition(i, 1).widget().text())

        exclude_dirs_str = ",".join(yd_exclude_dirs)
        yd_process = subprocess.Popen(
            ["yandex-disk", "start", f"--dir={yd_directory}", f"--exclude-dirs={exclude_dirs_str}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        while yd_process.poll() == None:
            time.sleep(0.5)
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