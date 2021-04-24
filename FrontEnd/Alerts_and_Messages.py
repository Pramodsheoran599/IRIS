# Importing Libraries
import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from qt_material import apply_stylesheet


class Alert(QMainWindow):
    def __init__(self):
        super(Alert, self).__init__()

        uic.loadUi(r"Ui Files\Alert_Window.ui", self)
        # Implement Alert Class


class Message_Box(QMainWindow):
    def __init__(self):
        super(Message_Box, self).__init__()

        uic.loadUi("Ui Files\\Message_Box.ui", self)

        self.message_icon = self.findChild(QLabel, "Message_Icon")
        self.message_label = self.findChild(QLabel, "Message_Label")

    def display(self, code, message):
        if code == "Success":
            qImg = QImage(r'Ui Files\Images\Success_Icon.png')

        else:
            qImg = QImage(r"Ui Files\Images\Error_Icon.png")

        self.message_label.setPixmap(QPixmap.fromImage(qImg))
        self.message_label.setText(message)


def Message(code, message):
    message_box = Message_Box()
    message_box.display(code, message)
    message_box.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Main Application
    app.setWindowIcon(QIcon("Ui Files\\Images\\Window_Icon"))  # Setting Application Icon
    apply_stylesheet(app, theme='dark_amber.xml')  # Setting Theme of Application

    alert_window = Alert()
    alert_window.show()

    sys.exit(app.exec_())
