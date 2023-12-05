
import sys
from PyQt5.QtCore import Qt, QEvent,QRect, QPropertyAnimation,QParallelAnimationGroup, QEasingCurve
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel,QStackedWidget, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.uic import loadUi
import resources
import Hashing_Password

class MainWindow_2(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Credentials.ui",self)
        self.SignUpBtn.clicked.connect(self.switch_to_signup_page)    
        self.LoginBtn2.clicked.connect(self.switch_to_login_page)
        self.SignUpBtn2.clicked.connect(self.signUp)
        self.LogInBtn.clicked.connect(self.signIn)

    def switch_to_login_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_signup_page(self):
        self.stackedWidget.setCurrentIndex(1) 

    def signIn(self):
        print('hey')
        name = self.username.toPlainText()
        password = self.password.toPlainText()
        print('hey')
        check = Hashing_Password.signIn(name, password)
        print('hey')
        if check:
            self.mainWindow = MainWindow()  
            self.mainWindow.show()


    def signUp(self):
        name = self.username_su.toPlainText()
        password = self.password_su.toPlainText()
        Hashing_Password.signUp(name, password)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("MainWindow.ui",self)  # Load your UI file here
        self.restoreIcon = QIcon(":/icons/icons/square.svg")
        self.maximizedIcon = QIcon("://icons//icons//copy.svg")
        # Remove default title bar and set window flags
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.titleBar = QWidget(self)
        
        self.restoreBtn.setIcon(self.restoreIcon)
        self.restoreBtn.clicked.connect(self.toggle_maximize)
        self.minimizeBtn.clicked.connect(self.minimize_window)
        self.closeBtn.clicked.connect(self.close_window)
         # Connect button signals to functions
        self.settingBtn.clicked.connect(self.show_settings)
        self.helpBtn.clicked.connect(self.show_help)

        # Initialize stacked widget
        self.leftStackedWidget.setCurrentIndex(0)  # Set the initial index of the stacked widget
        self.current_index = 0  # Variable to track the current index

        # # Get the stacked widget from the loaded UI
        # self.leftleftStackedWidget = self.findChild(QleftStackedWidget, "leftleftStackedWidget")

        # # Connect buttons to switch between stacked widgets
        # self.settingBtn.clicked.connect(lambda: self.change_page(0))
        # self.helpBtn.clicked.connect(lambda: self.change_page(1))



    def event(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMaximized():
                self.restoreBtn.setIcon(self.maximizedIcon)
            else:
                self.restoreBtn.setIcon(self.restoreIcon)
        return super().event(event)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def minimize_window(self):
        self.showMinimized()

    def close_window(self):
        self.close()

    # def change_page(self, index):
    #     current_index = self.leftleftStackedWidget.currentIndex()
    #     if index != current_index:
    #         start_geometry = self.leftleftStackedWidget.geometry()
    #         self.leftleftStackedWidget.setCurrentIndex(index)
    #         end_geometry = self.leftleftStackedWidget.geometry()

    #         # Create animation to slide between widgets
    #         self.slide_widget(self.leftleftStackedWidget, start_geometry, end_geometry)

    # def slide_widget(self, widget, start_geometry, end_geometry):
    #     # Create animation
    #     self.animation = QPropertyAnimation(widget, b"geometry")
    #     self.animation.setDuration(500)  # Set animation duration in milliseconds
    #     self.animation.setStartValue(start_geometry)
    #     self.animation.setEndValue(end_geometry)
    #     self.animation.setEasingCurve(QEasingCurve.InOutQuad)
    #     self.animation.start()


    
    def show_settings(self):
        if self.current_index != 0:
            self.slide_widget(0)
            self.current_index = 0

    def show_help(self):
        if self.current_index != 1:
            self.slide_widget(1)
            self.current_index = 1

    def slide_widget(self, index):
        current_widget = self.leftStackedWidget.currentWidget()
        target_widget = self.leftStackedWidget.widget(index)

        start_geometry = current_widget.geometry()
        end_geometry = target_widget.geometry()

        start_geometry.moveLeft(self.width())
        end_geometry.moveLeft(0)

        current_widget.setGeometry(start_geometry)
        target_widget.setGeometry(end_geometry)

        animation_current = QPropertyAnimation(current_widget, b"geometry")
        animation_current.setDuration(500)
        animation_current.setStartValue(start_geometry)
        animation_current.setEndValue(start_geometry.translated(self.width(), 0))
        animation_current.setEasingCurve(QEasingCurve.InOutQuad)

        animation_target = QPropertyAnimation(target_widget, b"geometry")
        animation_target.setDuration(500)
        animation_target.setStartValue(end_geometry.translated(-self.width(), 0))
        animation_target.setEndValue(end_geometry)
        animation_target.setEasingCurve(QEasingCurve.InOutQuad)

        group_animation = QParallelAnimationGroup()
        group_animation.addAnimation(animation_current)
        group_animation.addAnimation(animation_target)
        group_animation.start()

        self.leftStackedWidget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow_2()
    window.show()
    sys.exit(app.exec_())


