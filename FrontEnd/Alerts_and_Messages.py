# Importing Libraries
import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from qt_material import apply_stylesheet


class Alert(QMainWindow):
    def __init__(self):
        super(Alert, self).__init__()

        uic.loadUi(r"Ui Files\Alert_Window.ui", self)
        # Implement Alert Class


class Message_Box(QMainWindow):
    def __init__(self):
        super(Message_Box, self).__init__()

        uic.loadUi(r"Ui Files\Message_Box.ui", self)

        self.message_icon = self.findChild(QLabel, "Message_Icon")
        self.message_label = self.findChild(QLabel, "Message_Label")
        self.ok_btn = self.findChild(QPushButton, "OK_Button")

        self.ok_btn.clicked.connect(lambda: self.close())

    def display(self, code, message):

        if code == "Success":
            pixmap = QPixmap(r"Ui Files\Images\Success_Icon.png")

        else:
            pixmap = QPixmap(r"Ui Files\Images\Error_Icon.png")

        self.message_icon.setPixmap(pixmap)
        self.message_label.setText(message)


def Message(self, code, message):
    self.message_box = Message_Box()
    self.message_box.display(code, message)
    self.message_box.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Main Application
    app.setWindowIcon(QIcon(r"Ui Files\Images\Window_Icon"))  # Setting Application Icon
    apply_stylesheet(app, theme='dark_amber.xml')  # Setting Theme of Application

    alert_window = Alert()
    alert_window.show()

    sys.exit(app.exec_())
