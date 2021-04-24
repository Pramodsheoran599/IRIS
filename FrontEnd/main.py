import sys

from PyQt5 import QtCore, uic, QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet

from Home import Home_Window
from Login import Login_Window
from SignUp import SignUp_Window

counter = 0                                                                                 # Global Counter for Progress Bar percentage


class Splash_Screen(QMainWindow):                                                           # Splash Screen Class
    def __init__(self):
        super(Splash_Screen, self).__init__()

        uic.loadUi(r"Ui Files\Splash_Screen.ui", self)                                      # Loading the Ui File

        self.dropShadowFrame = self.findChild(QFrame, 'dropShadowFrame')                    # Drop Shadow Frame
        self.label_description = self.findChild(QLabel, 'Desc_Label')                       # Description Label
        self.progress_bar = self.findChild(QProgressBar, 'Progress_Bar')                    # Progress Bar

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)                                   # Removing Title Bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)                               # Translucent Background

        self.shadow = QGraphicsDropShadowEffect(self)                                       # Creating a Shadow
        self.shadow.setBlurRadius(200)                                                      # Blur Radius of Shadow
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.dropShadowFrame.setGraphicsEffect(self.shadow)                                 # Applying Shadow to Drop Shadow Frame

        self.timer = QtCore.QTimer()                                                        # Timer Object
        self.timer.timeout.connect(self.progress)
        self.timer.start(30)                                                                # Start Timer with 30 Millisecond delays

        # CHANGE DESCRIPTION
        # Initial Text
        self.label_description.setText("<strong>WELCOME</strong> TO MY APPLICATION")

        # Change Texts
        QtCore.QTimer.singleShot(1500, lambda: self.label_description.setText("<strong>CONNECTING TO </strong> DATABASE"))
        QtCore.QTimer.singleShot(3000, lambda: self.label_description.setText("<strong>SETTING UP</strong> USER INTERFACE"))

        self.show()

    def progress(self):
        global counter

        # SET VALUE TO PROGRESS BAR
        self.progress_bar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            apply_stylesheet(app, theme='dark_amber.xml')                                   # Setting Theme of Application
            window_stack.show()                                                             # Displaying the Window Stack

            self.close()                                                            # close splash screen

        counter += 1                                                            # Increasing the Progressbar Percentage


if __name__ == "__main__":
    app = QApplication(sys.argv)                                                         # MAIN APPLICATION
    Splash_window = Splash_Screen()
    app.setWindowIcon(QtGui.QIcon(r"Ui Files\Images\Window_Icon"))                       # SETTING APPLICATION ICON

    window_stack = QStackedWidget()                                                      # WINDOW STACK OBJECT FOR SWITCHING BETWEEN WINDOWS
    home_window = Home_Window(window_stack)                                              # HOME WINDOW OBJECT
    login_window = Login_Window(window_stack, home_window)                               # LOGIN WINDOW OBJECT
    signup_window = SignUp_Window(window_stack)                                          # REGISTER WINDOW OBJECT

    window_stack.setWindowTitle("Login")                                                 # SETTING TITLE OF STACK TO HOME
    window_stack.resize(640, 240)                                                        # DIMENSIONS OF LOGIN WINDOW

    window_stack.addWidget(login_window)                                                 # ADDING OBJECTS
    window_stack.addWidget(home_window)                                                  #     TO
    window_stack.addWidget(signup_window)                                                #  WINDOW STACK

    sys.exit(app.exec_())
