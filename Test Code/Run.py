from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from Login import Login_Window
from Home import Home_Window
from SignUp import Register_Window


class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(800, 480)

        self.QtStack = QtWidgets.QStackedLayout()

        self.login_window = Login_Window()
        self.home_window = Home_Window(self.QtStack)
        self.register_window = Register_Window(self.QtStack)

        # self.Window1UI()
        # self.Window2UI()
        # self.Window3UI()


        self.QtStack.addWidget(self.home_window)
        self.QtStack.addWidget(self.register_window)
        self.QtStack.addWidget(self.login_window)

    def Window1UI(self):
        self.stack1.resize(800, 480)

        # PushButton1#
        self.PushButton1 = QtWidgets.QPushButton(self.stack1)
        self.PushButton1.setText("BUTTON 1")
        self.PushButton1.setGeometry(QtCore.QRect(10, 10, 100, 100))

        # PushButton2#
        self.PushButton2 = QtWidgets.QPushButton(self.stack1)
        self.PushButton2.setText("BUTTON 2")
        self.PushButton2.setGeometry(QtCore.QRect(150, 150, 100, 100))

    def Window2UI(self):
        self.stack2.resize(800, 480)
        self.stack2.setStyleSheet("background: red")

    def Window3UI(self):
        self.stack3.resize(800, 480)
        self.stack3.setStyleSheet("background: blue")


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.QtStack = QtWidgets.QStackedLayout()

        self.login_window = Login_Window(self.QtStack)
        self.home_window = Home_Window(self.QtStack)
        self.register_window = Register_Window(self.QtStack)


        self.QtStack.addWidget(self.home_window)
        self.QtStack.addWidget(self.register_window)
        self.QtStack.addWidget(self.login_window)

        self.QtStack.setCurrentIndex(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main()
    sys.exit(app.exec_())