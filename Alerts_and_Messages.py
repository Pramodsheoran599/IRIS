from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap, QImage


class Alert(QtWidgets.QMainWindow):
    def __init__(self):
        super(Alert, self).__init()

        uic.loadUi("UI\\Alert_Window.ui")
        self.show()

        # Implement Alert Class


class Message_Box(QtWidgets.QMainWindow):
    def __init__(self):
        super(Message_Box, self).__init__()

        uic.loadUi("UI\\Message_Box.ui", self)

        self.message_icon = self.findChild(QtWidgets.QLabel, "Message_Icon")
        self.message_label = self.findChild(QtWidgets.QLabel, "Message_Label")

    def display(self, code, message):
        if code == "Success":
            qImg = QImage('UI\\Images\\Success_Icon.png')

        else:
            qImg = QImage("UI\\Images\\Error_Icon.png")

        self.message_label.setPixmap(QPixmap.fromImage(qImg))
        print("ss")
        self.message_label.setText(message)
        print("ss")


def Message(code, message):
    message_box = Message_Box()
    message_box.display(code, message)
    message_box.show()
